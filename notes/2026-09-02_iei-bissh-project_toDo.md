### IEI-BISSH pipeline: to do (dev work)
### Julian Moran
### 2026-09-02



1. Create best-of-both worlds approach in `feature/integrate_diverged`
- branch 1: `dev`
- branch 2: `feature/composite_score`

Merge status:
```
1. E-value annotation
- Keep <=0.05 filter from `feature/pymol_composite`
  - otherwise conform to `dev`'s asset flow, column naming convention, ETL
  - status: COMPLETE

2. PyMOL-super alignment results capture
- Keep tsv sidecar bugfix from `feature/pymol_composite`
  - i.e. throw out fallback stdout check logic
  - i.e. throw out pull of Calpha atoms
  - i.e. throw out coverage guard computation
  - i.e. throw out decoupling of AlphaFold download and alignment
  - otherwise keep pull of aligned residues
  - otherwise keep `dev`'s persistent structure cache
  - otherwise conform to `dev`'s asset flow, ETL
  - status: COMPLETE

3. TM-align alignment
- `feature/pymol_composite` supersedes but needs to conform to `dev`'s ETL
    - i.e. throw out low-pLDDT-masked TM-align run
    - i.e. throw out align-span pLDDT means
    - i.e. throw out disorder flag
    - status: COMPLETE


4. Composite scoring annotation
- `feature/pymol_composite` supersedes but needs to conform to `dev`'s ETL
    - use `feature`'s updated composite weightings and parameters
    - read composite weightings and parameters solely from root .env

5. Caching retrieved PDB structures
- `feature/pymol_composite` supersedes but needs to conform to `dev`'s ETL
    - i.e. keep DuckDB alignment results cache
    - additionally, keep a permanent cache of all retrieved structures (@juliandeanmoran: does `dev` do this? confirm)
    - additionally, update DuckDB with `bacteria_pdb` and `human_pdb` fields
    - additionally, those fields should give the file location of the pdb structures in the structure cache

6. Data feed from data -> [backend?] -> frontend lefthand navigator
- `feature/pymol_composite` supersedes but needs to conform to `dev`'s ETL
    - i.e. just feed the new composite score from data-> frontend

7. Composite display on frontend righthand per-pair panel
- update `dev`'s backend  to compute new composite score in real-time
    - pass to per-pair righthand panels
    - read composite weightings and parameters solely from root .env
    - ensure root .env reached backend at runtime; i.e. no dockerignore
```


2. Improve gene name annotation in `final_output`
- i.e. query the UniParc db for all accessions that do not get a gene name (this is currently 33% of the results)