### BISSH meeting notes
### 2026-08-28
### Julian Moran


# Attendees

1. Stephen Scherer
2. Chantel Trost
3. Christian Marshal
4. Vinicius Furlan
5. Julian Moran


# Prep

### Protein pairs of interest

1. Pairs showcasing PyMOL-super's utility
	- txt
	- txt
	- txt

2. Pairs passing positive control
	- No pairs in the positive control set from literature are present in this dataset
	- Half-pairs:
		+ Q8WXG1:A0A330LKB8 # A0A330LKB8 is viperin, which is expected
		+ I8UTJ7:*			# we expected ThsA and didn't find it


I have confirmed your analysis results. We have three unique gold-standard human proteins (Q8WXG1, Q8N884, Q9BPY3) that appear in the composite scored dataset two unique gold-standard bacterial defense system proteins (D5EID4, Q6XGD5).

We now need to determine why we do not see a D5EID4:Q8WXG1 pair or a Q6XGD5:Q8N884 pair in the composite score dataset. May you please tell me the e-value for these two pairs? Please remember that our e-value dataset is between repIDs, so you will have to find their repIDs first.


┌─────────┬───────────┬────────────┐
│ Protein │   Role    │   repID    │
├─────────┼───────────┼────────────┤
│ D5EID4  │ bacterial │ A0A2E7NAI8 │
├─────────┼───────────┼────────────┤
│ Q8WXG1  │ human     │ A0A1I8IYD6 │
├─────────┼───────────┼────────────┤
│ Q6XGD5  │ bacterial │ A0A7X7LFC8 │
├─────────┼───────────┼────────────┤
│ Q8N884  │ human     │ A0A7R8YNI5 │
└─────────┴───────────┴────────────┘

3. Pairs showing high composite, low sequence alignment
	- Q17R31-A0A7V1GEN9
	- Q6P1N9-Z9JIC9
	- Q9Y530-A0A562WL79
	- Q6ICS7-A0A143HJQ2	# >1400 bacterial hits for Q6ICS7
	- Q6ICS7-A0A0F7VVX1 # "
	- Q6ICS7-A0A1X0VBH1 # "
	- A0A7P0TB94-A0A509EDC2 # and domain alignment


4. Domain-specific alignment
	- Q9Y530-Q5KV84
	- Q8TBC4-L0L0B2
	- Q8TBC4-A0A5J6WSX9
	- B2RBP3-L0L0B2



### Recurring human proteins

1. Q6ICS7 - DNMT2
	- tRNA methyltransferase
	- "No Orthology or Paralogy data is available from the Alliance of Genome Resources."
	- >1400 bacterial matches
	- >1400 bacterial matches for O14717 (TRDMT - tRNA methyltransferase) also 

2. Q53FP3 - DND
	- cystein desulfurase
	- catalyzes the desulfuration of L-cysteine to L-alanine as component of the cysteine desulfurase complex

3. Q9Y3B8 - REXO2
	- mitochondrial oligoribonuclease
	- 3'-to-5'exoribonuclease that preferentially degrades DNA and RNA oligonucleotides composed of only two nucleotides

4. Q2VPJ6 - HSP90A1
	- heat shock chaperone


Big categories in top 100:
- HSP90
- RNA / DNA helicases
- Cysteine sulferases / lysases
- tRNA methyltransferase



# Blasting proteins

- psiBLAST -- position-specific iterative BLAST
	+ use domain-specific
	+ beware of same protein with different e-values with each iteration (i.e. results will be duplicated -- take the lowest e-value)


# To do from meetings

1. Systematic pairwise BLAST

2. Systematic abstract search
	- `f"{bact_gene_name) homologous to {hs_gene_name}" >> bool`
	- `f"{hs_gene_name} has immune function?" >> bool`

3. Gold set: use gene names instead of UniProt

4. Make chromosomal map of high-score sets



# Ideal publication threshold

1. Use this tool
2. Diagnose new cases
>> American Journal of X (5 to 15 impact factor)


1. Use this tool
2. Find this new system in humans (Vinicius)
>> Nature (>15 impact factor)