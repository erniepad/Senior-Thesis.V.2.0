# author: JImmy Gonzalez Nunez
# We study the phase-space diagram for the survival probabilities and invading species population fraction.

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm


# read data from file 'ensemble.data', containing (s, b, mu, rho_m)
dataFile = "mean.csv"

data = pd.read_csv(dataFile, sep=",", names=[":time", ":ypos", ":xpos"])



# create b-mu-rho phase-diagram
queryFrame = data.groupby([":time"])[":xpos"].std().reset_index()


print(queryFrame)

#plt.scatter(queryFrame[":time"], np.sqrt(queryFrame[":xpos"]))






#Calculate Roughening Exponent 
j =  2
i =  4
time_evol = []
boundary_evol = []
while i <= 220:
    vt =  (np.log((queryFrame[":xpos"][i] / queryFrame[":xpos"][j])) / np.log(queryFrame[":time"][i] / queryFrame[":time"][j]) )
    time = np.log10(queryFrame[":time"][i]) 
    i = i + 1
    j = i // 2
    time_evol.append(i)
    boundary_evol.append(vt)
    

print(len(boundary_evol))
print(len(time_evol))





plt.scatter(time_evol, boundary_evol)

#plt.plot(queryFrame[":time"], queryFrame[":xpos"])
plt.show()