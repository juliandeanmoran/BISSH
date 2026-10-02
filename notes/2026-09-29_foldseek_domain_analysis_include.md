### Should we include FoldSeek domain dataset?
### Julian Moran
### 2026-09-29

# Context

- IEI-BISSH pipeline is missing important gold-standard protein pairs
- C Trost: will including the FoldSeek domain analysis set help pick them up?


# Foldseek domain analysis protocol
1. intake: repID sequences

2. all-v-all structural similarity search using foldseek
  - likely the same or trivially different from main analysis network

3. for each sequence ...
  - filter for pairs with `e_value <= 10e-3`
  - hierarchically cluster start and end position of each foldseek hit (here, they are clustering alignments for each protein against all others)
  - with network, filter for domains (clusters) with `span <= 350 AAs`
  - with network, filter for domains (clusters) with `>= 5 nodes`
  - with network, filter for edges with `e_value <= 10e-5`
  - etc...


# Methods -- notes
1. The text isn't clear whether they're using the exact same repID all-v-all network as the main Foldseek analysis
  - however, it is still a all-v-all network of repIDs
  - however, it is still a network computed by the same Foldseek protocol
  - therefore, network used is either exact same or trivially different (e.g. different computational run)
  - therefore, this will not expose new pairwise alignments missed by our pipeline

2. Threshold used is `e_value <= 10e-3`
  - less lenient than our pipeline's of `e_value <= 0.05`
  - therefore, this will not expose new pairwise aligmments missed by our pipeline

3. start and end positions clustered ussing hierarchical clustering
  - alignments were first trimmed using `span <= 350 AAs`
  - hierarchical clustering height parameter of 250 (again, it's every specific protein P <--> x, where x can be any other protein)
  - this was used to define consensus alignmed domains
  - this is the sole unique part of this analysis that our pipeline does not inclue
  - this is also not really relevant to our research question
  - i.e., this will not exposre new pairwise alignments missed by our pipeline


# Conclusion
- We should not include the FoldSeek domain-specific alignment dataset