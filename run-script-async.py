# author: JImmy Gonzalez Nunez
# simple script to fun program on each of the available cores
import os
import platform
import subprocess
import multiprocessing as mp
import time
import numpy as np
import argparse


def run_template(vars):
    "executes command/terminal command {cline}"
    s, b, mu, lx, ly = vars

    cline = f"python main.py --lx {lx} --ly {ly} --b {b} --mu {mu} --s {s}"

    if platform.system() == "Linux":
        cline = f"nice python main.py --lx {lx} --ly {ly} --b {b} --mu {mu} --s {s} "

    os.system(cline)
    print("finsihed command: ", cline)


def print_result(res):
    print(res)


def print_args(x):
    time.sleep(1)
    print(x)
    return x

if __name__ == "__main__":
    mp.freeze_support()

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--lx", type=int, default=10)
    parser.add_argument("--ly", type=int, default=10)

    parser.add_argument("--reserveCores", type=int, default=50)

    parser.add_argument("--trials", type=int, default=2)

    #b is the selective advantage of bystander over slow growing strain 
    parser.add_argument("--b_max", type=float, default=0.00)
    parser.add_argument("--b_min", type=float, default=0.05)
    parser.add_argument("--b_num", type=int, default=1)
    
    #s is the measure of the deleterious effect of the mutation
    parser.add_argument("--s_max", type=float, default=0.0)
    parser.add_argument("--s_min", type=float, default=0.0)
    parser.add_argument("--s_num", type=int, default=1)

    #mu is the mutation rate of the deleterious mutation 
    parser.add_argument("--mu_min", type=float, default=0.00)
    parser.add_argument("--mu_max", type=float, default=0.00)
    parser.add_argument("--mu_num", type=int, default=1)

    args = parser.parse_args()

    # paramters
    p = mp.Pool(processes=mp.cpu_count() - args.reserveCores)

    s_max = args.s_max
    s_min = args.s_min
    s_num = args.s_num

    mu_min = args.mu_min
    mu_max = args.mu_max
    mu_num = args.mu_num

    b_min = args.b_min
    b_max = args.b_max
    b_num = args.b_num

    lx = args.lx
    ly = args.ly

    trials = args.trials

    # create list of argument values, passed to run_template
    l = [(s, b, m, lx, ly) for s in np.linspace(s_min, s_max, s_num) for b in np.linspace(b_min, b_max, b_num) for m in np.linspace(mu_min, mu_max, mu_num) for _ in range(trials)]


    if args.reserveCores < 2:
        print("please allow for two cores to be unused")
        exit()
    print(f"running with {mp.cpu_count()-args.reserveCores} processes")

    # start processing pool and queue each command line process
    start = time.time()
    p.map_async(run_template, l)
    p.close()
    p.join()
    end = time.time()
    print("async time: ", end - start)


