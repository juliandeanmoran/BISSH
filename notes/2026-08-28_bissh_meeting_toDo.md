### BISSH project: to do
### Julian Moran
### 2026-08-28


# Software dev

1. Merge

2. Add term to composite that penalises bad matches


# Data science

0. Use the domain-specific FoldSeek dataset in pipeline
	- status: COMPLETE

1. Systematic pairwise BLAST
    - plot BLASTp score against composite score (?)
	- status: COMPLETE

2. Systematic abstract search
	- `f"{bact_gene_name) homologous to {hs_gene_name}" >> bool`
	- `f"{hs_gene_name} has immune function?" >> bool`
	- i.e. cursory GPT-5-mediated lit review of high-scoring protein pairs

3. Gold set comparison: use gene names instead of UniProt

4. Make chromosomal map of high-score sets

5. Distinguish between domain-specific overlaps and full overlaps
	- add penalizations

6. Merge branches
	- status: COMPLETE

7. Conduct a pathway analysis of the gene list