from ConstrainGA import ConstrainGA
from ConstrainPSO import ConstrainPSO
from FiberModelOpt.FiberModelRunner import *
import numpy as np


def target_func(h2,gap,d,cost_concrete=400/1000000,cost_steel=35000/1000000):
    Ac,As = design_factors_area(h2,gap,d)
    return Ac*cost_concrete+cost_steel*As

def constrain_1_capacity(h2,gap,d):
    load = 10.5
    l = 20
    calculated_moment,self_weight_load = design_factors_load_and_resistenace(h2,gap,d)
    load_total = load+self_weight_load
    needed_moment = load_total*l*l/8*1e3*1e3
    return calculated_moment-needed_moment

if __name__ == "__main__":
    boundary = [[200,1000],[100,200],[10,26]]
    GA_params = {
        "pop_size":100,
        "iteration_num":10,
        "mutation_prob_limit":0.05
    }
    CGA = ConstrainGA()
    CGA.set_boundary(boundary)
    CGA.set_algorithm_param(**GA_params)
    CGA.set_target_func(target_func)
    CGA.set_constraint_func([constrain_1_capacity,])
    CGA.run(multi_thread=True)
    # CGA.run()
