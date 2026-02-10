### BISSH: analysts strategy 1
### Julian Moran
### 2026-02-09


# C Trost proposal

```
Dear Vinicius and Julian,

I hope you both had a relaxing weekend and stayed warm.

I think we should touch base on Friday, since we will be meeting with Steve and Christian the following week.

In preparation for our next meeting, please familiarize yourself with the datasets. Since Anjali has actually produced a lot of results thus far, I think it would be fun to take a look at some of the available data and try to answer some of the following questions.

	What are the best human matches for each bacterial defense system protein? We could start by considering those matches that are closest in amino acid length. For example, if a single domain bacterial protein WP_100000000.1, belongs to cluster XXX, and is 100 aa long, and its closest human match is AXE0000000.1, belongs to cluster XXY, and is 113 aa long, then we would want to output this to a new file and label this human protein as a "top match." **Please note that there may be multiple human proteins belonging to cluster XXY, all of slightly varying lengths, so it is important to retain all of them. Also, we need to retain relevant information about these matches (such as the e-value between the clusters, functional annotations, protein length, number of domains, etc.), so please be sure to copy identifying information and document your work well.**

    Are there any themes among the human matches that correspond to a given bacterial defense system? For example, domains, biological functions, biochemical pathways, etc. 

    Are there any themes among the human matches, such as clustering within a particular human gene region or chromosome? These could correspond to a given bacterial defense system or not.

    For Steve, let's work backwards and see if we can identify autism-associated genes in the Foldseek clusters (these may or may not be in our current output). Are there any bacterial proteins in the same cluster? What about in closely related clusters? What is their presumed biological role? **Recall that bacterial proteins are often poorly annotated, so it is okay to put together a guess, but do not spend lots of time validating your guesses until I meet with you. At this time, I will provide guidance on how best to go about this.**


This is not a comprehensive list of questions we will want to address, but rather a starting point. 

To review the matches and assess if they make sense (think small scale manual validation for now), you can use PyMOL (https://www.pymol.org/). It's freely available and easy to use. Also, there are loads of tutorials and help pages for it. You will want to focus on obtaining one metric (the Root Mean Squared Deviation (RMSD) score) from your structural overlays. This metric can be "massaged" a bit to obtained better values, but this requires a little bit more effort. There are tutorials online for this too. If you have relatively good overlays (4 Angstroms or less), then don't worry about this for now. If you have okay overlays (4-12 Angstroms), you can work on optimizing them. A good RMSD for a small protein will be very small (<2). A good RMSD for a large protein complex can be very large (>4). ***Keep this in mind.***

Let me know when you are ready to create PyMOL images that don't have watermarks on them. I will cover the cost of the paid version at this time. In the meantime, there are work arounds to generate image for presentations without having to pay a usage fee. I can show you some tricks if you need help.

I think AlphaFold (the online server) also allows for structural alignments to be made, but I have not played with it for over a year now. It may be even easier to use than PyMOL. I think it also provides RMSD scores, but I am not sure how to optimize them using this tool.

There are other software options for viewing and analyzing structures too, so feel free to try out a few. 

Sincerely,

Chantel

P.S. Christian and Steve are likely to ask you questions about conserved residues. Please think about what conserved amino acid residues in our study might reflect. Do we ignore differences? 

P.P.S. Also, think carefully about how you report your results. Are you reporting a protein match or a gene match (or both)? People will interpret your results in different ways depending on how you report them. 

P.P.P.S. We can discuss how to visualize your preliminary results on Friday. Please come prepared to have this conversation. Examples would be helpful here.
```