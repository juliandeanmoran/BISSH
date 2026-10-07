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
	- status: COMPLETE

4. Make chromosomal map of high-score sets

5. Distinguish between domain-specific overlaps and full overlaps
	- add penalizations

6. Merge branches
	- status: COMPLETE

7. Conduct a pathway analysis of the gene list

8. Go back and check ...
	- how does the pipeline handle cluster members <---> repIDs?
	- ... obviously the pipeline ingests all-v-all repIdS
	- ... does it ever map back from repIDs --> cluster members?
	- if answer is no, how come we have e-values of 0 in our dataset, where 0 indicates same repID?
	- talk to Opus about this


9. Gold set comparison part 2: recover loss due to cluster members <---> repIDs
	- do 8. first
	- then implement this algorithm:
```
Foldseek: recover more gold-standard pairs by ...
    a. converting gold standard proteins to repIDs
    b. converting those repIDs to gene names
    c. seeing if those gene names have a pair in my `composite_score` df
```


10. Gold set comparison part 3: recover loss due to DefenseFinder's limited coverage
	- do 9. first, and if gold standard recovery is not good ...
```
DefenseFinder: recover more gold-standard pairs by ...
	a. map gold-standard accessions back to DefenseFinder accessions that are sequence-homologous 
```


11. Send out the data to C Marshall
    - IUIS-IEI annotation with > 0.85
    - subset: low-sequence homology, high composite score (composite score > 0.85), annotate with IUIS-IEI