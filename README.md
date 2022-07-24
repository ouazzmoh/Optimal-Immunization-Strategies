# Optimal-Immunization-Strategies
This script concludes a research work that I have done about the optimization of immunization strategies.
The script models the population as a Scale free network using the Barabasi-Albert algorithm.
It compares the spread of a pandemic using 3 different vaccination techniques:
	1. Random: Choosing randomly the nodes to vaccinate.
	2. Targeted: Choosing the nodes with the highest degrees to vaccinate.
	3. Acquaintance Immunization: Choosing a random group of nodes, choosing random nodes from their neighbors and immunizing them.
The result show that the Targeted stategy gives the best results and the random strategy gives the worst results, however the targeted strategy is a techniquethat's quite difficult to realise. The acquaintace immunization gives us a middle ground between the two.
For more information and theoritical analysis of the strategies refer to the following paper---> DOI: 10.1140/epjb/e2004-00119-8



