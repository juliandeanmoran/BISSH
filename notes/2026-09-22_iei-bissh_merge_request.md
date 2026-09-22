`Feature/integrate_diverged` reconciles `dev` with `feature/pymol_composite`, creating a best-of-both-worlds approach.

### Major changes:

1. At e-value annotation, protein pairs are filtered for `e_value <= 0.05`
    - i.e. the minimum threshold of significance while ignoring multiple hypothesis correction
    - otherwise conforms to `dev`'s asset flow, column naming convention, and ETL framework

2. Updated PyMOL-super alignment results capture protocol
    - couples AlphaFold model download and alignment so that they occur on the same compute node (confirmed working)
    - keeps tsv sidecar results capture from `feature/pymol_composite`, which `dev` also already implements
    - keeps `dev`'s capture of aligned residues
    - keeps `dev`'s persistent structure cache
    - deprecates `dev`'s fallback stdout check logic: redundant and needless complexity; stdout will never contain the results
    - deprecates `dev`'s capture of Calpha atoms: currently not used in downstream computation
    - deprecates `dev`'s coverage guard computation: if we are going to incorporate a coverage guard check, this logic should be integrated into the composite score so that everything is in one place
    - otherwise conforms to `dev`'s asset flow, column naming convention, and ETL framework

3. Updated TM-align results capture protocol
    - deprecates `dev`'s low-pLDDT-masked TM-align run
    - deprecates `dev`'s align-span pLDDT mean capture
    - deprecates `dev`'s disorder flag
    - otherwise conforms to `dev`'s asset flow, column naming convention, and ETL framework

4. New composite scoring logic
    - applies `feature/pymol_composite`'s linear-weighted, six-term composite scoring function, which includes a sinusoidal transformation of the PyMOL RMSD and saturating-growth transformation of the Foldseek e-value
    - all features and parameters are read from root .env
    - composite annotations are incorporated into pipeline final output file

5. Allignment results metrics are now stored in a library DuckDB
   - alignment run logic is only performed on pairs that have not been aligned previously
   - additionally retains `dev`'s cache of PDB structures (called the PDB mirror in the code base)
   - additionally, DuckDB library has new fields for `bacteria_pdb` and `human_pdb`, which store the individual PDB file locations for each alignment result (`feature/pymol_composite`'s library lacked these)
   - additionally, DuckDB has new fields for `pymol_aligned_residues` and `aligned-span` (`feature/pymol_composite`'s library lacked these)
   - deprecated `dev`'s --from-scratch flag for alignment; alignment can be performed from scratch by manually wiping the PDB mirror and the library DuckDB; since these are more intentional acts, this is more appropriate for a destructive and potentially irreversible cache-wipe operation

6. Frontend updates
    - frontend lefthand navigator now ranks by composite score rather than TM-align q-value; composite score is displayed instead
    - frontend righthand details panel now shows foldseek e-value on topmost banner
    - frontend righthand details panel now ranks Structural Analogs Matches table rows by composite score, which is now displayed as leftmost column in the table
    - frontend now contains minor changes to spelling and mouse-over text phrasing for clarity and accuracy
    - deprecated lefthand navigator mouse-over text

7. PyMOL is managed by conda instead of uv during Dagster pipeline run
    - applies workaround of uv environment with `uv sync --frozen --no-install-package pymol-open-source`
    - therefore PyMOL still under uv management as well
    - consider deprecating uv'smanagement of PyMOL in the future

8. Deprecated parity testing
    - seems vestigial from pyspark --> DuckDB ETL refactor
    - maintaining it against ongoing changes to the code is painful

9. Condensed `data/README.md`, removed 1000s of lines from in-script comments and doc strings
    - pipeline README is now much more succinct and quickly conveys major features, asset flow, run protocol, data publish protocol, and major dependencies
    - in-script comments and doc-strings have been overhauled to emphasise the "what" rather than the "how"
        + i.e. emphasis on input-output contracts
        + i.e. de-emphasis of mechanism; code itself conveys this better
        + i.e. de-emphasis of things the code no longer does or problems the code avoids, as the set of these is indefinitely large