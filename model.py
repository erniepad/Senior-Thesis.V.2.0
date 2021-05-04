# author: Jimmy Gonzalez Nunez
# date: 27 Oct, 2020
import numpy as np
from numpy import log
from random import uniform, choice
import tools as utils
from itertools import accumulate


class Lattice:
    def __init__(self, lx, ly):
        self.time = np.zeros((lx, ly))
        self.filled = np.full((lx, ly), False, dtype=bool)
        self.ids = np.full((lx, ly), -1, dtype=int)
        self.sqrlat = [(1, 0), (-1, 0), (0, 1), (0, -1)]  #! using this for now
        self.adjNodes = {
            0: [(1, 0), (-1, 0), (-1, -1), (0, -1), (-1, 1), (0, 1)],
            1: [(1, 0), (-1, 0), (0, 1), (1, 1), (0, -1), (1, -1)],
        }
        self.lx = lx
        self.ly = ly

    def IsFilled(self, x, y):
        return self.filled[x, y]

    def FillSite(self, x, y, gid, time):
        self.filled[x, y] = True
        self.ids[x, y] = gid
        self.time[x, y] = time


class RangeExpansionMutationsModel(Lattice):
    def __init__(self, lx, ly):
        super().__init__(lx, ly)
        self.pops = dict()
        self.rates = dict()
        self.startTimes = dict()
        self.simTime = 0.0
        self.nMutations = 0
        self.mutations = 0
        self.gRates = dict()
        self.finished = False

    def PrintExperimentInfo(self, params):
        description = """
        This model implements an eden growth model, with event
        selection via Gillespie algorithm. Mutations appears at
        fixed locations, upto a maxium nMutations.
        """
        print(description)
        print("simulation info:")
        for param in params.keys():
            print(f"   --{param}: {params[param]}")
        for gid, subpop in self.pops.items():
            print(f"  -- subpopulation {gid} of size {len(subpop.arr)}")

    def SetModelParams(self, params):
        self.rates = params["rates"]
        self.nMutations = params["nMutations"]
        self.mu = params["mu"]

    def CheckParams(self):
        if self.nMutations > len(self.rates):
            raise Exception("-> insufficient rates given for mutations needed")
        for gid, subpop in self.pops.items():
            if len(subpop.arr) == 0:
                raise Exception(f"-> subpopulation {gid} is empty")

    def InsertParticle(self, x, y, gid):
        if gid not in self.pops:
            self.pops[gid] = utils.FArray()
        self.pops[gid].insert((x, y))
        self.FillSite(x, y, gid, self.simTime)
    
    # def InsertPoint(self, x, y, gid): 
    #     if gid not in self.pops: 
    #         self.pops[gid] = utils.FArray()
    #         print(len(self.pops[1]))
    #     self.pops[1].insert((x, y))
    #     self.FillSite(x, y, gid, self.simTime)

    def Nbors(self, x, y):
        for dx, dy in self.sqrlat:  #! swtiched to sqaure lattice
            if x + dx >= 0:
                nx = dx + x
                ny = (dy + self.ly + y) % self.ly
                if not self.IsFilled(nx, ny):
                    yield (nx, ny)

    def Replication(self):
        r, g = zip(
            *(
                (subpop.size() * self.rates[gid], gid)
                for gid, subpop in self.pops.items()
            )
        )
        rs = list(accumulate(r))
        R = rs[-1]
        rn = uniform(0, 1) * R
        val = next((x for x in rs if rn <= x), None)
        return R, g[rs.index(val)]

    def Grow(self, x, y, nx, ny, gidx):
        "currently doesn't not mutate cell, but can be added here"
        if x == nx and y == ny:
            raise Exception("error in replicating")
        gidx == 0
        self.InsertParticle(nx, ny, gidx)
        if gidx == 1 and uniform(0, 1) < self.mu:
            gidx = 2
        self.InsertParticle(nx, ny, gidx)
        # self.FillSite(nx, ny, gidx, self.simTime)
        # self.pops[gidx].insert((nx, ny))

    # def mutantPoint(self, x, y, nx, ny, gidx): 
    #     gidx = 1
    #     self.InsertPoint(nx, ny, gidx)

    def EndCondition(self, x, y, wtype=0):
        # TODO :add support for colliding colonies
        if wtype == 0:
            if x == self.lx - 3:
                self.finished = True
                return

    def Update(self):
        R, gidx = self.Replication()
        if gidx is None:
            raise Exception("check event selection algorithm")
        element = self.pops[gidx].random()
        if element is None:
            raise Exception("Check for empty sub populations")
        x, y = element
        nbors = list(self.Nbors(x, y))
        if len(nbors) <= 1:
            self.pops[gidx].remove(element)
        # if len(nbors) == 1: 
        #     self.simTime += -log(uniform(0, 1)) / R
        #     nx, ny = choice(nbors)
        #     self.mutantPoint
        if len(nbors) >= 1:
            self.simTime += -log(uniform(0, 1)) / R
            nx, ny = choice(nbors)
            self.Grow(x, y, nx, ny, gidx)
        self.EndCondition(x, y)

    def GetSubPopulation(self, gid):
        return self.pops[gid].arr

    

