# author: JImmy Gonzalez Nunez
# We study the phase-space diagram for the survival probabilities and invading species population fraction.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# read data from file 'ensemble.data', containing (s, b, mu, rho_m)
dataFile = "testiy.data"

data = pd.read_csv(dataFile, sep=" ", names=[":b", ":mu", ":rhom"])

# create b-mu-rho phase-diagram
queryFrame = data.groupby([":b", ":mu"])[":rhom"].mean().reset_index()


data = pd.read_csv(dataFile, sep=" ", names=[":b", ":mu", ":rho_m"])

# create b-mu-rho phase-diagram
queryFrame = data.groupby([":b", ":mu"])[":rho_m"].mean().reset_index()


# print the data table to stdout
print(queryFrame)


# create phase diagram
XYZ = [(v[0], v[1], v[2]) for v in queryFrame.values]
b, m, p = zip(*XYZ)

def mf(m):
    return 0.3*(1 - 0.5*(m/(0.3**2)))

def cri(m): 
    return 0.3 - m


murange = np.linspace(0.0, 0.2, num=50)
#MF = [mf(m) for m in murange]
# CF = [cri(m) for m in murange]


fig, ax = plt.subplots()
#sc = ax.scatter(m, b, c=p, marker="s", vmin=0.0, vmax=1.0, cmap=cm.plasma_r)
sc, = ax.plot(p,b)
#ax.scatter(murange, MF)
# ax.scatter(murange, CF)


ax.set_ylim(0.0, 0.3)
plt.ylabel('Selective Advantage of Bystander')

ax.set_xlim(0.0, 0.12)
plt.xlabel('Mutation Rate')

plt.colorbar(sc).set_label("$\\rho_m$")

plt.show()
