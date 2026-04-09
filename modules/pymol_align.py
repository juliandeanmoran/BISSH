import logging
import os
import pymol2
import requests
import subprocess
import tempfile
import time

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict

import polars as pl

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
#       AlphaFold structures
# ────────────────────────────────────────────────────────────

def get_alphafold_structure(
        uniprot_id: str,
        out_dir: Path,
        api_endpoint: str,
        wait_time: float = 1.0,
        overwrite: bool = False,
) -> str | None:
    
    # Check if file already exists:
    out_file = out_dir / f"{uniprot_id}_AF.pdb"
    if os.path.exists(out_file) and not overwrite:
        logger.warning(f"For {uniprot_id}, ALphaFold structure is already on file at {out_file}.")
        return str(out_file)
    else:
        out_file = str(out_file)

    time.sleep(wait_time)
    url = f"{api_endpoint}/{uniprot_id}"
    logger.info(url)
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.warning(f"For {uniprot_id}, failed to retrieve: {e}")
        return None
    url_pdb = response.json()[0].get("pdbUrl", None)

    if url_pdb is not None:
        logger.info(f"For {uniprot_id}, retrieving .pdb from {url_pdb}...")
        try:
            response = requests.get(url_pdb)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"For {uniprot_id}, failed to retrieve: {e}")
            return None

        with open(out_file, "wb") as f:
            f.write(response.content)
        logger.info(f"For {uniprot_id}, AlphaFold predicted structure written to {out_file}.")
        return out_file
    
    else:
        logger.warning(f"For {uniprot_id}, AlphaFold structure not found.")
        return None


def get_alphafold_structures(
    df_uniprot_ids: pl.DataFrame,
    col_query_uniprot_id: str,
    col_target_uniprot_id: str,
    out_dir: Path,
    api_endpoint: str,
    wait_time: float = 1.0,
    overwrite: bool = False,
) -> tuple[pl.DataFrame, str, str]:
    
    # Initialize column structures
    col_query_structure_file_name = "Bacterial_protein_AF_file"
    col_target_structure_file_name = "Human_protein_AF_file"
    col_query_structure_file, col_target_structure_file = [], []

    for i in range(len(df_uniprot_ids)):
        
        logger.info("============================================================")
        logger.info("Query protein:")

        # Query proteins
        query_protein_structure_file = get_alphafold_structure(
            uniprot_id=df_uniprot_ids[i, col_query_uniprot_id],
            out_dir=out_dir,
            api_endpoint=api_endpoint,
            wait_time=wait_time,
            overwrite=overwrite
        )
        col_query_structure_file.append(query_protein_structure_file)

        logger.info("")
        logger.info("Target protein:")

        # Target proteins
        target_protein_structure_file = get_alphafold_structure(
            uniprot_id=df_uniprot_ids[i, col_target_uniprot_id],
            out_dir=out_dir,
            api_endpoint=api_endpoint,
            wait_time=wait_time
        )
        col_target_structure_file.append(target_protein_structure_file)
    
    # Annotate file name to data
    df = df_uniprot_ids.with_columns(
        pl.Series(col_query_structure_file_name, col_query_structure_file)
    ).with_columns(
        pl.Series(col_target_structure_file_name, col_target_structure_file)
    )

    logger.info("============================================================")
    return df, col_query_structure_file_name, col_target_structure_file_name


# ────────────────────────────────────────────────────────────
#       PyMol: pairwise alignment
# ────────────────────────────────────────────────────────────

def pymol_align_pair(
    pdb_query: str,
    pdb_target: str,
    out_path_structure: str,
    pymol_align_method: str,
    overwrite: bool = False,
) -> tuple[str, str]:
    
    # Check if alignment file already exists
    if os.path.exists(out_path_structure) and not overwrite:
        logger.warning(f"For {pdb_query}, {pdb_target} PyMol alignment is already on file at {out_path_structure}. Add overwrite=True if you wish to run alignment again.")
        return None, None

    pymol_script = f"""
from pymol import cmd

cmd.load(r"{pdb_query}", "s1")
cmd.load(r"{pdb_target}", "s2")

cmd.hide("everything")
cmd.show("cartoon", "s1")
cmd.show("cartoon", "s2")
cmd.color("blue", "s1")
cmd.color("red", "s2")

r = cmd.{pymol_align_method}("s1", "s2")

print("METRICS\\t%f\\t%d" % (r[0], r[1]))
cmd.save(r"{out_path_structure}")
cmd.quit()
"""

    # Run alignment
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(pymol_script)
        script_path = tmp.name
    result = subprocess.run(
        ["pymol", "-cq", script_path],
        capture_output=True,
        text=True,
        check=True,
    )

    logger.info(f"For {pdb_query},{pdb_target}, wrote alignment results to {out_path_structure}.")

    # Capture alignment performance metrics
    rmsd = None
    aligned_atoms = None

    for line in result.stdout.splitlines():
        if line.startswith("METRICS"):
            _, rmsd, aligned_atoms = line.split("\t")
            rmsd = float(rmsd)
            aligned_atoms = int(aligned_atoms)
    return rmsd, aligned_atoms


def pymol_align_pairs(
    df_structure_files: pl.DataFrame,
    col_query_id: str,
    col_query_struct: str,
    col_target_id: str,
    col_target_struct: str,
    out_dir: str,
    pymol_align_method: str,
    overwrite: bool = False,
) -> tuple[pl.DataFrame, str]:
    
    col_struct_paths, col_rmsd, col_aligned_atoms = [], [], []

    for i in range(len(df_structure_files)):
        query_id = df_structure_files[i, col_query_id]
        target_id = df_structure_files[i, col_target_id]
        out_path_structure = f"{out_dir}/{query_id}_{target_id}_aligned.pse"

        rmsd, aligned_atoms = pymol_align_pair(
            pdb_query=df_structure_files[i, col_query_struct],
            pdb_target=df_structure_files[i, col_target_struct],
            out_path_structure=out_path_structure,
            pymol_align_method=pymol_align_method,
            overwrite=overwrite
        )
        col_struct_paths.append(out_path_structure)
        col_rmsd.append(rmsd)
        col_aligned_atoms.append(aligned_atoms)
    
    col_pse = "PyMOL_aligned_filePath"
    df = df_structure_files.with_columns(
        pl.Series(col_pse, col_struct_paths)
    ).with_columns(
        pl.Series("PyMOL_RMSD", col_rmsd)
    ).with_columns(
        pl.Series("PyMOL_aligned_atoms", col_aligned_atoms)
    )
    return df, col_pse


# ────────────────────────────────────────────────────────────
#       PyMol: render to PNG
# ────────────────────────────────────────────────────────────

def render_pse(
        pse_path: Path,
        query_id: str,
        target_id: str,
        out_dir: Path,
        width=1200,
        height=900,
        dpi=300,
        render_single_proteins: bool = False,
        overwrite: bool = False,
        evade_watermark: int = None
    ) -> None:
    with pymol2.PyMOL() as pymol:

        out_path = out_dir / f"{query_id}_{target_id}_aligned.png"

        if not overwrite and Path(out_path).exists():
            logger.warning(f"Overwrite is {overwrite} and {out_path} already exists.")
            logger.warning(f"For {query_id}, {target_id}, aborting capture(s) ...")
            return None

        cmd = pymol.cmd
        cmd.reinitialize()
        cmd.load(str(pse_path))

        # Configure scene
        cmd.bg_color("white")
        cmd.hide("everything", "all")
        cmd.show("cartoon", "all")
        cmd.orient()

        cmd.set("ray_opaque_background", 0)
        cmd.set("antialias", 2)

        # Render pairwise alignment
        cmd.ray(width, height)
        cmd.png(str(out_path), dpi=dpi)
        logger.info(f"For {query_id}, {target_id}, wrote capture to {out_path}.")

        if render_single_proteins:
            out_path_s1 = out_dir / f"{query_id}_{target_id}_aligned_s1_{query_id}.png"
            out_path_s2 = out_dir / f"{query_id}_{target_id}_aligned_s2_{target_id}.png"

            objs = cmd.get_object_list("all")
            if len(objs) < 2:
                logger.error(f"Expected ≥2 objects, found {len(objs)}")
                logger.error(f"For {query_id}, {target_id}, aborting s1, s2 captures ...")
                return None

            s1, s2 = objs[:2]

            # Render structure 1 (bacterial)
            cmd.disable("all")
            cmd.enable(s1)

            if evade_watermark is not None:
                cmd.zoom(s1, buffer=evade_watermark + 10)
                cmd.move("y", -evade_watermark)

            cmd.ray(width, height)
            cmd.png(str(out_path_s1), dpi=dpi)
            logger.info(f"For {query_id}, wrote s1 capture to {out_path_s1}.")

            # Render structure 2 (human)
            cmd.disable("all")
            cmd.enable(s2)
            cmd.ray(width, height)

            cmd.png(str(out_path_s2), dpi=dpi)
            logger.info(f"For {target_id}, wrote s2 capture to {out_path_s2}.")
        return None
    
def render_pses(
    df_pse: pl.DataFrame,
    col_pse: str,
    col_query_id: str,
    col_target_id: str,
    out_dir: Path,
    dpi: int = 300,
    render_single_proteins: bool = False,
    overwrite: bool = False,
    evade_watermark: int = None
) -> None:
    
    for i in range(len(df_pse)):
        query_id = df_pse[i, col_query_id]
        target_id = df_pse[i, col_target_id]
        pse_path = df_pse[i, col_pse]

        render_pse(
            pse_path=pse_path,
            query_id=query_id,
            target_id=target_id,
            out_dir=out_dir,
            dpi=dpi,
            overwrite=overwrite,
            render_single_proteins=render_single_proteins,
            evade_watermark=evade_watermark
        )
    return None