from mwapy import aocal
import numpy as np


def nan_helper(y):
	return np.isnan(y), lambda z: z.nonzero()[0]


ao = aocal.fromfile("1134156736_model-HydA-58comp_withalpha_solutions.bin")

for tile in range(128):
	tileSolution = ao[0,tile,:,:]
	#The below is the list of tiles to be flagged
	if tile in [4, 19, 52, 73, 78, 88, 105, 107, 115, 118, 122, 125] :
		continue
	nans, x = nan_helper(tileSolution)
	tileSolution[nans] = np.interp(x(nans), x(~nans), tileSolution[~nans])
	print("working on tile " + str(tile))	
	ao[0,tile,:,:] = tileSolution

ao.tofile("newSolutionV2.bin")



