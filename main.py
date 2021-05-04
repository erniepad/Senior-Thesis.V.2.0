# author: Jimmy Gonzalez Nunez
import model as model
import numpy as np
import matplotlib.pyplot as plt
import initialconditions as initcnd
import time
import boundary_msd
import tools
import argparse
import random
import math
from matplotlib.pyplot import cm
from celluloid import Camera
import pandas as pd
from matplotlib.colors import ListedColormap

# **************************
parser = argparse.ArgumentParser()
parser.add_argument("--b", type=float, default=0.2)
parser.add_argument("--s", type=float, default=0.3)
parser.add_argument("--mu", type=float, default=0.2)
parser.add_argument("--mutations", type=int, default=0)
parser.add_argument("--lx", type=int, default=100)
parser.add_argument("--ly", type=int, default=100)
parser.add_argument("--frames", type=int, default=10)
parser.add_argument("--animate", action="store_true", help="create animation")
parser.add_argument("--save", action="store_true", help="save results")
parser.add_argument("--plotFigures", action="store_true")
parser.add_argument("--info", action="store_true")
parser.add_argument("--test", action="store_true")
parser.add_argument("--trilattice", action="store_true")
parser.add_argument("--name", default="boundaries")
parser.add_argument("--saveLandscape", action="store_true")
args = parser.parse_args()
# **************************
params = dict()
params["lx"] = args.lx
params["ly"] = args.ly
params["nMutations"] = args.mutations
params["rates"] = {0: 1 - args.s + args.b , 1: 1, 2: 1.0  -args.s}
params["mu"] = args.mu
cpf = (args.lx * args.ly) / args.frames
# **************************
# TODO :add linear fit, then use slope in MSD calculation
random.seed(time.time())
#***************************


# **************************
timeStamp = time.strftime("Date-%Y-%m-%d-Time-%H-%M", time.localtime())
programDir = tools.SetDir(f"../Samples/")
MediaDir = tools.SetDir(f"{programDir}/media")
OutputDir = tools.SetDir(f"{programDir}/output")

# **************************
exprmt = model.RangeExpansionMutationsModel(args.lx, args.ly)
exprmt.SetModelParams(params)
# Use for mixed population 
bndrycon = initcnd.Line(0, args.ly, exprmt, config="split", boundary="non-periodic")
# Use for a single point species 
#initcnd.Point(args.ly // 2, args.ly, exprmt)

exprmt.CheckParams()
if args.info:
    exprmt.PrintExperimentInfo(params)

# **************************
plt.style.use("bmh")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.4, 6.4))
fig.tight_layout()
ax.axis("on")
ax.set_xlim(0, args.ly)
ax.set_ylim(0, args.lx)
ax.set_xlabel("y")
ax.set_ylabel("x")
camera = Camera(fig)
# *************************

colors = {
    -1: "white",
    0: "yellow",
    1: "red",
    2: "black"
}

colors = ListedColormap(["white", "yellow", "red", "black"])

#colors = ListedColormap(colors)

cnt = 0
while True:
    if exprmt.finished:
        break
    exprmt.Update()
    cnt += 1
    if args.animate and cnt == cpf:
        ax.imshow(
            exprmt.ids,
            origin="lower",
            cmap=colors
            #cmap=cm.hot,
            #vmin=-1,
           # vmax=params["nMutations"] + 2,
        )
        camera.snap()
        cnt = 0

if args.info and (args.save or args.plotFigures):
    with open(f"{MediaDir}/RunInfo-{timeStamp}.txt", "w") as file:
        for param in params.keys():
            file.write(f"  --{param}: {params[param]}\n")

if args.animate:
    print(f" > creating animations...", end="\r")
    anim = camera.animate()
    if args.save:
        anim.save(f"{MediaDir}/animation-{timeStamp}.gif", writer="ffmpeg", fps=24)
        print(f" > finished creating animations in {MediaDir}")
    else:
        print(f" > finished creating animations, appearing soon")
        plt.show()


if args.save:
    if args.info:
        print(f" > saving some data in {OutputDir}")
    reg, L, msd = boundary_msd.MSDReferenceScaling(bndry, rho=dist)
    if reg.rvalue > 0.75:
        ns = [exprmt.pops[gid].size() for gid in range(2)]
        with open(f"{OutputDir}/{args.name}.data", "a") as file:
            file.write(f"{reg.slope}, {ns[0]/(sum(ns))}, {args.g2-1.0}\n")

if args.plotFigures:
    import custom_plots

    bndry = boundary_msd.FindBoundary(exprmt.ids, args.lx, args.ly, window=20)
    #tx = [(exprmt.time[xy[0],xy[1]], xy[0], xy[1]) for xy in bndry]
    #print(tx)
    xx, yy = zip(*bndry)
    bfit = boundary_msd.stats.linregress(xx, yy)
    m = 0 
    # dist = lambda x0, y0: abs(-bfit.slope * x0 + y0 - bfit.intercept) / (np.hypot(bfit.slope, 1))
    dist = lambda x0, y0: abs(-m * x0 + y0 - args.ly / 2) / (np.hypot(m, 1))

    msd = boundary_msd.MSD2D(bndry, dist)
    fit = boundary_msd.MSDFit(msd)
    print("slope", fit.slope)
    msdFig, msdax = custom_plots.MSDPlot(msd, fit, MediaDir, saveFig=args.save)
    gridFig, gridax = custom_plots.GridSpace(exprmt, bndry, m)

    if not args.save:
        plt.show()

#Generates the mean sector boundary 
if exprmt.finished == True: 
    bndry = boundary_msd.FindBoundary(exprmt.ids, args.lx, args.ly, window=20)
    tx = [(math.floor(exprmt.time[xy[0],xy[1]]), xy[0], xy[1]) for xy in bndry]
    df = pd.DataFrame(tx, columns= ["Time", "ypos", "Pos"] )
    with open("mean.csv", "a") as file:
        df.to_csv(file,header= False, index= False)


#Creates survival of mutation  
if exprmt.finished == True: 
    if exprmt.pops[1].size() == 0 or exprmt.pops[2] == 0:
        prob = 0
    else: 
        prob = 1
    with open("survival.data", "a") as file:
        file.write(f"{args.b} {args.mu} {prob}\n")

#Calculates fraction of fast-invader 
if exprmt.finished == True: 
    phi_f = (exprmt.pops[1].size() )/sum(pop.size() for pop in exprmt.pops.values())
    with open ("phi.data", "a") as file: 
        file.write(f"{args.b} {args.mu} {phi_f}\n")


#rho_m --> 1 - wildtype
# rho_m = 1 - (exprmt.pops[0].size() )/sum(pop.size() for pop in exprmt.pops.values())
# # check f-strings in python
# with open("testiy.data", "a") as file:    
#     file.write(f"{args.b} {args.mu} {rho_m}\n")
