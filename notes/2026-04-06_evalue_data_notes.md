### e-value data field notes
### Julian Moran
### 2026-04-06


# Conclusions

1. Use `evalue_foldseek` for global similarity between bacterial protein and human protein
2. Use `evalue` for similarity between bacterial cluster and human cluster


# From A Jain

Hi Julian,

I hope you’re doing well and my apologies for the delayed response!

If I remember correctly, the `evalue` field comes from the `6-all-vs-all-similarity-queryId_targetId_eValue.tsv.gz` file and represents the similarity e-value of the foldseek clusters. The `evalue_foldseek` field comes from the local foldseek output and represents the similarity of the bacterial and human protein in the row.

As an example, let’s use the file 2025-07-27_zorya_annotated.xlsx and filter for A0A4P6HK41 as the bacterial protein (column J). This bacterial protein belongs to Foldseek cluster A0A1W9LKN2 (col K), which is associated with the human cluster A0A3Q0EX91 (col L). These two clusters have an e‑value of 0.066 (column N).

The human cluster A0A3Q0EX91 contains six human proteins (col M): Q7Z726, B7Z979, P52292, A8K7D9, A0A7I2V487, and F5GZT0.

To obtain pairwise e‑values between the bacterial protein and each human protein, I ran Foldseek locally. Those results are recorded in columns P–Y, with one set of values for each bacterial–human protein pair.

```
defense_system_protein_id	defense_system_cluster_id	cluster_id	protein_id	evalue	cluFlag	fident	alnlen	mismatch	gapopen	qstart	qend	tstart	tend	evalue_foldseek
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	Q7Z726	0.066	1	0.114	455	327	0	34	488	5	374	0.1295
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	B7Z979	0.066	2	0.119	381	322	0	25	405	1	366	0.1802
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	P52292	0.066	1	0.105	385	302	0	34	418	5	342	0.2206
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	A8K7D9	0.066	1	0.095	387	304	0	32	418	6	342	0.3575
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	A0A7I2V487	0.066	1	0.098	357	296	0	62	418	14	342	0.1235
A0A4P6HK41	A0A1W9LKN2	A0A3Q0EX91	F5GZT0	0.066	1	0.118	369	287	0	8	376	14	339	3.603
```


I hope this helps and answers your questions! Please let me know if anything is unclear.

Thanks,
Anjali