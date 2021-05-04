import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np


def MSDPlot(msd, fit=None, dir="../Samples/media/", fName="test", saveFig=False):
    fig, ax = plt.subplots()
    ax.loglog(range(len(msd)), msd, "ro")
    ax.set_xlabel("steps")
    ax.set_ylabel("MSD")
    if fit is not None:
        ax.loglog([np.exp(fit.intercept)*n**fit.slope for n in range(len(msd))], label = rf"$m={fit.slope}$")
        plt.legend()
    if saveFig:
        fig.savefig(f"{dir}/{fName}.png")
    return fig, ax


def GridSpace(model, boundary, slope=None):
    fig, ax = plt.subplots()
    ax.imshow(
        model.ids,
        origin="lower",
        cmap=cm.gist_ncar,
        vmin=-1,
        vmax=model.nMutations + 2,
    )
    bx, by = zip(*boundary)
    ax.plot(by, bx, "o")
    if slope is not None:
        ax.plot([model.ly/2 + slope*x for x in range(model.lx)], [x for x in range(model.lx)], "r+")
    ax.set_xlim(0, model.ly)
    ax.set_ylim(0, model.lx)
    ax.set_xlabel("y")
    ax.set_ylabel("x")
    return fig, ax