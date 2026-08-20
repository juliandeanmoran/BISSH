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