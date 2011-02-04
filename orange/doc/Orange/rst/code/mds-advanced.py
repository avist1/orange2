# Description: Advanced MDS test: 1000 optimization iterations, stress calculation after every 10th
# Category:    projection
# Uses:        iris
# Referenced:  Orange.projection.mds
# Classes:     Orange.projection.mds.MDS

import Orange
import math

# Load some data
table = Orange.data.Table("iris.tab")

# Construct a distance matrix using Euclidean distance
dist = Orange.core.ExamplesDistanceConstructor_Euclidean(table)
matrix = Orange.core.SymMatrix(len(table))
for i in range(len(table)):
   for j in range(i+1):
       matrix[i, j] = dist(table[i], table[j])

# Run the Torgerson approximation and calculate stress
mds = Orange.projection.mds.MDS(matrix)
mds.Torgerson()
mds.calcStress(Orange.projection.mds.KruskalStress)

# Optimization loop; calculate the stress only after each 10 optimization steps:
for i in range(100):
    oldStress = mds.avgStress
    for j in range(10):
        mds.SMACOFstep()

    mds.calcStress(Orange.projection.mds.KruskalStress)
    if oldStress * 1e-3 > math.fabs(oldStress - mds.avgStress):
        break

# Print the points out
for (p, e) in zip(mds.points, table):
    print p, e