### BISSH meeting notes
### Julian Moran
### 2026-04-27


# Participants

1. J Moran
2. C Trost
3. V Furlan


# Feature requests -- review from last meeting

1. Fix ribbon view
  - possibly by changing what we call it

2. Incorporate PDB solved-structure utility
  - do we account for it in the score

3. Confirm SMARCA4, BTAF1

4. Structural alignment superimposed on sequence
  - apparently V Furlan already added this
  - need to toggle between them
  - need to get toggle

5. Need something beyond pairwise comparisons
  - whole-cluster structural alignment superimposed on sequences

6. Make bacterial names orange
  - make bacterial structures orange

7. Add annotations for data
  - disease / condition annotatios for human
  - bacterial system annotations for bacteria
  - immune-related (y / n) for all

8. Have TM-align

9. BIG: have structural alignent view

10. BIG: have PPI
  - which hman proteins interact with hman proteins?
  - which bacterial proteins interact with bacterial proteins?
  - where are or databases for the above? 

11. BIG: have multimer
  - builds on CBlast



# QC -- check that these are in the Zorya dataset

1. SMARC4A (human protein)
2. DDX1 (human protein)
3. BTAF (human protein)

- Where is Zorya?
  + get some Zorya proteins and confirm they are in the dataset frontend
  + if the answer is yes, why don't we see 1., 2., 3.


# Message

It is the dreaded this:

`git pull --all`
>>
```
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
```

I am on my `main` branch. The divergent branches modify different files, so they should be mergeable. What is the bash syntax for proceeding with the merge?
