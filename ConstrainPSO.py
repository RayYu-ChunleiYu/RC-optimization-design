import numpy as np 
from typing import List
from State import State
from ConstrainAlg import ConstrainAlg

class ConstrainPSO(ConstrainAlg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def pops_evaluate(self,pops:List[State]):
    def pops_evaluate(self,pop:State):
        values = pop.get_values()
        pop.update_f_value(self.target_func(*values))
        constrain_break = 0
        for constrain_func in self.constrain_funcs:
            if constrain_func(*values) < 0:
                constrain_break += 1
        pop.update_constrain_break(constrain_break)
        extra_info = pop.get_extra_info()
        # update single pop
        if pop.get_constrain_break() < extra_info['best_constrain_break']:
            extra_info['best_constrain_break'] = pop.get_constrain_break()
            extra_info['best_values'] = pop.get_values()
            extra_info['best_f_value'] = pop.get_f_value()
        elif pop.get_constrain_break() == extra_info['best_constrain_break']:
            if pop.get_f_value() < extra_info['best_f_value']:
                extra_info['best_values'] = pop.get_values()
                extra_info['best_f_value'] = pop.get_f_value()
    
    def run(self,extra_info = None,multi_thread = False):
        extra_info = {
            "best_values":np.zeros(len(self.boundary)),
            "best_f_values":np.inf,
            "best_constrain_break":100000,
            "velocity":np.zeros(len(self.boundary)),
        }
        super().run(extra_info,multi_thread)


    def next_generation_generate(self,pops:List[State]):
        w = self.algorithm_param['w']
        c1 = self.algorithm_param['c1']
        c2 = self.algorithm_param['c2']
        next_gen = []
        for pop in pops:
            # update velocity
            extra_info = pop.get_extra_info()
            best_values = extra_info['best_values']
            congnitive = c1 * np.random.rand() * (best_values - pop.get_values())
            social = c2 * np.random.rand() * (self.global_best_values - pop.get_values())
            velocity = w*extra_info['velocity']+congnitive+social
            # update position
            pop.update_value(pop.get_values()+velocity)
            self.bounds_constrain(pop)
            next_gen.append(pop)
        return next_gen

if __name__ == "__main__":
    boundary = [[0,1],[2,3]]
    target_func = lambda x1,x2:(x1-0.8)**2+(x2-2.5)**2
    constrain_func_1 = lambda x1,x2:x1-0.9
    CPSO= ConstrainPSO()
    CPSO.set_boundary(boundary)
    CPSO.set_target_func(target_func)
    CPSO.set_constraint_func(constrain_func_1)
    PSO_param = {
        "pop_size": 30,
        "iteration_num": 100,
        "w": 0.3,
        "c1": 1.4,
        "c2": 1.4,
    }
    CPSO.set_algorithm_param(**PSO_param)
    CPSO.run()