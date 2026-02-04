### Notes: Hernandez 2023
### Julian Moran
### 2026-02-04


# Introduction

Take-aways
- FoldSeek is innovative because it is fast
- Compares 214 million structures against each other in 5 days on 64 cores


# Structure-based clustering of the AFDB

E-value
- Pairwise sequence alignment concept
- Given alignment score `S` for query sequence `q` ...
	+ where `q` is `m`-long
	+ where the reference database is `n`-long (i.e. the length of all sequences in the database summated)
	+ how many hits would we observe to `q`, with a score of `S` or greater, due to random chance?

- E.g. For `m`-long sequence `q` with score `S` against `n`-long db, `E = 0.01`
	+ therefore, there is only a 1% chance of observing a random hit this good
	+ therefore, we can reasonably conclude the hit is due to genuine evolution-related homology 

50% sequence identity
- 2 proteins cluster together iff >=50% of their aligned regions match perfectly

90% sequence overlap
- 2 proteins cluster together iff >=90% of the shorter protein is implicated in alignment

Highest-pLDDT representative
- pLDDT (predicted local distance difference test): AlphaFold's confidence score for 3D structure
- therefore, use the highest quality structure prediction for the representative
