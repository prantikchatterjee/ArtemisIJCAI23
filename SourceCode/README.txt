ARTEMIS Readme

Requirements:
Python 3.7+
scipy
numpy
csv
Linux environment

System Used To Run The Experiments:
i5-8300h Processor
16 GB RAM
Ubuntu 18.04

Spectrum generation:
We have used the following open-source repositories for generating the spectrums. The procedure for setting up the toolchain is detailed in the respective repositories.
1. Evosuite: https://github.com/prantikchatterjee/evosuite.git/tree/ulysis (used for generating test-suites using evolutionary search).
2. Defects4J: https://github.com/prantikchatterjee/defects4j/tree/prantik-exps (the Defetc4J dataset that includes scripts for generating spectrums).
3. Ground truth for Defects4J: https://bitbucket.org/rjust/fault-localization-data/src/master/ (contains the ground truths for the Defects4J faults).

Data Preprocessing:
To ease the overhead of computation, each spectrum is reduced before the execution of Artemis by grouping the components which has the exact same pattern into a single one. Components with the same patterns will always have the same SBFL score by any metric, hence, one score computaion per group of same component is sufficient. During the exam score and rank computation, the groups are again broken down into individual components to provide the accurate developer effort. The processEvoSpectrums.py script is used to preprocess the spectrums and map the ground truths.

Description Of ARTEMIS:
1. artemis.py: This implements the explorer, simulate and merge procedures given in Algorithms 1, 2 and 3 respectively. For convenience, explorer and simulate is implemented in the same procedure.
2. metrics.py: This implements the base SBFL metrics, i.e., Ochiai, Dstar2, Dstar3, Kulczynski, Tarantula, Op2 and Barinel, that were used in the paper.
3. parameterSelection.py: This implements the grid search for the optimal value of mu, beta and p for each Artemis variant.


