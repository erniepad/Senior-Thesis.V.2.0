import numpy as np
from scipy import stats


def MSD2D(traj, rho, offset=None):
    # time averaged msd
    if offset is None:
        offset = lambda x, y: y
    dismnts = [rho(x0, offset(x0, y0)) for x0, y0 in traj]
    numSteps = len(traj)
    msd = np.zeros(numSteps, dtype=float)
    for n in range(numSteps):
        displacement = 0.0
        for m in range(numSteps - n):
            displacement += (dismnts[n + m] - dismnts[m]) ** 2
        msd[n] = displacement / (numSteps - n)
    return msd


def MSD1D(trajx):
    # time averaged msd
    numSteps = len(trajx)
    msd = np.zeros(numSteps, dtype=float)
    for n in range(0, numSteps):
        displacement = 0.0
        for m in range(numSteps - n):
            displacement += (trajx[n + m] - trajx[m]) ** 2
        msd[n] = displacement / (numSteps - n)
    return msd


def MSDFit(msd, frac=0.85):
    # find first instance great than 5, otherwise start at pos 2
    stop = int(frac * len(msd))
    start = next((x for x in range(len(msd)) if msd[x] > 0), 2)
    X = np.log(range(start, stop))
    Y = np.log(msd[start:stop])
    return stats.linregress(X, Y)


def FindBoundary(grid, lx, ly, window=4):
    bndry = []
    y0 = -1
    for y in range(ly - 1):
        if grid[0, y] != grid[0, y + 1] and grid[0, y] == 0:
            y0 = y
    if y0 == -1:
        return np.array([])
    for x in range(lx):
        for y in range(y0 - window // 2, 1 + y0 + window // 2):
            if not 0 <= y < ly:
                continue
            if (
                grid[x, y] != grid[x, y + 1]
                and grid[x, y] != -1
                and grid[x, y + 1] != -1
            ):
                bndry.append((x, y))
                y0 = y
                break
    return np.array(bndry)