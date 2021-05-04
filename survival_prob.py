import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# read data from file 'ensemble.data', containing (s, b, mu, rho_m)
dataFile = "survival.data"

data = pd.read_csv(dataFile, sep=" ", names=[":b", ":mu", ":prob"])

# create b-mu-rho phase-diagram
queryFrame = data.groupby([":b", ":mu"])[":prob"].mean().reset_index()


data = pd.read_csv(dataFile, sep=" ", names=[":b", ":mu", ":prob"])

# create b-mu-rho phase-diagram
queryFrame = data.groupby([":b", ":mu"])[":prob"].mean().reset_index()


# print the data table to stdout
print(queryFrame)


# create phase diagram
XYZ = [(v[0], v[1], v[2]) for v in queryFrame.values]
b, m, p = zip(*XYZ)

def mf(m):
    return 0.3*(1 - 0.5*(m/(0.3**2)))


murange = np.linspace(0.0, 0.2, num=50)
MF = [mf(m) for m in murange]

fig, ax = plt.subplots()
sc = ax.scatter(m, b, c=p, marker="s", vmin=0.0, vmax=1.0, cmap=cm.plasma_r)
#ax.scatter(murange, MF)


ax.set_ylim(0.0, 0.3)
plt.ylabel('Selective Advantage of Bystander')

ax.set_xlim(0.0, 0.2)
plt.xlabel('Mutation Rate')


plt.colorbar(sc).set_label("$P_m$")
plt.show()