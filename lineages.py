from tools import FArray

class Lineages:
    def __init__(self):
        # TODO :add coalesnce calculations
        # TODO :add surviving lineages counts
        # TODO :add inherited label to calc number of surviving sectors
        pass

    def FillLineage(self, x, y, k, gid):
        """helper function for 'DetermineLineages'"""
        n = 0
        if not self.lineages[k][gid].insert((x, y, k)):
            return 0
        ax, ay, ak = self.ancestor[x, y, k]
        while ax != -1:
            if not self.lineages[k][gid].insert((ax, ay, ak)):
                n = 1
                break
            ax, ay, ak = self.ancestor[ax, ay, ak]
        return n

    def DetermineLineages(self):
        """calculate the lineages, automatically removing duplicates"""
        splitting = {0: 0, 1: 0}
        for strat, layercol in self.boundaries.items():
            for gid, subcol in layercol.items():
                for element in subcol.arr:
                    x, y, k = element
                    if k != strat:
                        raise Exception(" ! check lineages")
                    splitting[gid] += self._FillLineage(x, y, k, gid)
        return splitting, self.time
