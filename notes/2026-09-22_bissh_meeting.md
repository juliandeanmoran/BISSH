### BISSH project: to do
### Julian Moran
### 2026-08-28


# To do from past meeting

1. Use the domain-specific FoldSeek dataset

2. Systematic pairwise BLAST

3. Systematic abstract search
    - `f"{bact_gene_name) homologous to {hs_gene_name}" >> bool`
    - `f"{hs_gene_name} has immune function?" >> bool`

4. Gold set: use gene names instead of UniProt

5. Make chromosomal map of high-score sets

6. Distinguish between domain-specific overlaps and full overlaps
    - add penalizations



# To do from this meeting

1. Get top hits, stratify by below
    - Pathway analysis for paper
    - Bacterial Defense System
    - BioGRIID (protein-protein interaction)
    - disease analysis (OMIM)

2. Share the list in the OneDrive

3. Helicases
    - can we identify subclusters by structural homology




# Vinicius items

1. Zorya something

2. GNAT KMeans clustering algorithm

3. Features
    - search for bacteria of interest
    - considering two views in the UI
        + i.e. two categories of pages
        + i.e. get toggle for changing modes for the frontend
        + i.e. use colour coding

4. After running cBLASTer, GNAT
    - run PDB search for stoichiometry after finding a relationship
    - [why are we running cBLAST instead of structural homology tool]