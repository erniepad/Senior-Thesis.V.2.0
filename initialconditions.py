from random import choice


def Line(pos, width, model, config="split", boundary="side-periodic", vert=True):
    if config == "split":
        gids = lambda loc: 0 if loc < (model.ly // 2) else 1
    elif config == "mixed":
        gids = lambda loc: choice([0, 1])
    else:
        gids = 0
    spos = model.ly // 2 if vert else model.lx // 2
    for w in range(spos - width // 2, spos + width // 2):
        if vert:
            model.InsertParticle(pos, w, gids(w))
        else:
            model.InsertParticle(w, pos, gids(w))

    # boundary conditions
    if boundary == "side-periodic":
        bndryCon = {0: False, 1: True, 2: True, 3: False}
    else:
        bndryCon = {0: False, 1: False, 2: False, 3: False}
    return bndryCon


def Point(pos, width, model): 
    for w in range(0, model.ly):
        gid = 0 if w != pos else 1
        model.InsertParticle(0, w, gid)


def Circle():
    pass
