### IEI meeting 1
### Julian Moran
### 2026-02-19


Generate a BAM file indicating where aligned regions
- overlay with auto-inflammatory disorder variants
- would need to map back to protein isoform
- how many of these are already on gene lists (good positive control)? then the interesting ones are not


Follow up with Mike Tyers about domain overlay


Functional assay time
- ???

Very interested in sequence identity given high structural conservation


When you have candidate variants
- take patient's variant
- predict it with AlphaFold with the variant(s)
- is structure perturbed?


# Two end-games

1. Clinical genomics
- generate BED file of all genomic coordinates with structural homology to bactieral immune proteins
- intersect with variant calls from patients of any disease of interest
    + conduct burden analysis
    + e.g. disease: IEI (inborn errors of immunity)


2. Basic science hypothesis generation
- flag H.s. proteins that align to bacterial structure but have uncharacterised function
- flag H.S. protein domains that do not align and have no characterised function (requires domain overlay)
- feed into functional assay collaborators