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

Algorithm -- steps
1. MMSeq2
- 50% sequence identity
- 90% sequence alignment

2. Structural alignment 
- adapted LinClust, MMSeq2 to 3Di interaction structural alphabet


3Di sequence
1. For nearest spatial neighbor residues `i` and `j`, compute following unit vectors:
- where `C_alpha` denotes AA backbone carbon
- i.e. carbon between amine and carboxyl carbons
```
u1: C_alpha_i-1 --> C_alpha_i 
u2: C_alpha_i+1 --> C_alpha_i
u3: C_alpha_j-1 --> C_alpha_j 
u4: C_alpha_j+1 --> C_alpha_j
u5: C_alpha_i --> C_alpha_j
```

2. Compute following 10 features:
- where e.g. `cos(theta_12)` denotes cosine of angle between `u1`, `u2`
- where `sign()` returns ...
	+ +1 if positive
	+ -1 if negative
	+ 0 if 0
```
|C_alpha_i - C_alpha_k|
cos(theta_12)
cos(theta_34)
cos(theta_15)
cos(theta_35)
cos(theta_14)
cos(theta_23)
cos(theta_13)
sign(i − j) * min(|i − j|, 4)
sign(i − j) * log(|i − j| + 1)
```

3. Pass into autoencoder / decoder pair
- discrete latent state between encoder and decoder gives 3Di alphabet code
- training task:
	+ consider aligned residues `x` and `y`
	+ given 10-feature descriptor `x_n` for residue `x` ...
	+ what is the 10-feature descriptor for `y_n`?