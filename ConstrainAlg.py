
import numpy as np 
from typing import Callable,List
from tqdm import tqdm
from State import State
from abc import ABC, abstractmethod
import threading


class ConstrainAlg(ABC):
    def __init__(self, **kwargs):
        pass
        self.target_func = None;
        self.constrain_funcs:List[callable]  =[]
        self.boundary:List[list[float]] = []
        self.algorithm_param = {}
        self.pops:List[State] = []
        self.global_best_f_value = np.inf
        self.global_best_values=np.zeros(len(self.boundary))
        self.global_best_constrain_break = 100000


    def set_target_func(self,func:Callable):
        self.target_func = func

    def set_constraint_func(self,func):
        if isinstance(func,List):
            self.constrain_funcs.extend(func)
        elif isinstance(func,Callable):
            self.constrain_funcs.append(func)
        else:
            raise ValueError("func must be callable or list of callables")
    
    def bounds_constrain(self,pop:State):
        values = pop.get_values()
        for i in range(len(values)):
            if values[i] < self.boundary[i][0]:
                values[i] = self.boundary[i][0]
            elif values[i] > self.boundary[i][1]:
                values[i] = self.boundary[i][1]
        pop.update_value(values)

    def set_boundary(self,boundary:List[List[float]]):
        self.boundary = boundary
        self.global_best_values=np.zeros(len(self.boundary))

    # def set_algorithm_param(self,pop_size:int=50,iteration_num:int=100,w:float=0.7,c1:float=1.4,c2:float=1.4):
    def set_algorithm_param(self,**kwargs):
        self.algorithm_param = kwargs

    def run(self,extra_info = None,multi_thread = False):
        pops = [State(self.boundary,extra_info=extra_info) for _ in range(self.algorithm_param['pop_size'])]
        iter_num = self.algorithm_param['iteration_num']
        for i,_ in tqdm(enumerate(range(iter_num))):
            pops = self.next_generation_generate(pops)
            if multi_thread:
                threads = []
                for pop in pops:
                    thread = threading.Thread(target=self.pops_evaluate,args=(pop,))
                    threads.append(thread)
                    thread.start()
                for thread in threads:
                    thread.join()
            else:
                for pop in pops:
                    self.pops_evaluate(pop)
            self.global_update(pops)
            if i%(iter_num//5) == 0:
                print(f"{self.global_best_values} -> {self.global_best_f_value} with {self.global_best_constrain_break} constrain break")
        constrains_value = []
        for constrain_func in self.constrain_funcs:
            constrains_value.append(constrain_func(*self.global_best_values))
        print(f"{self.global_best_values} -> {self.global_best_f_value} with {self.global_best_constrain_break} constrain break")
        print(f"{constrains_value=}")

    def global_update(self,pops:List[State]):
        for pop in pops:
            if pop.get_constrain_break() < self.global_best_constrain_break:
                self.global_best_constrain_break = pop.get_constrain_break()
                self.global_best_values = pop.get_values()
                self.global_best_f_value = pop.get_f_value()
            elif pop.get_constrain_break() == self.global_best_constrain_break:
                if pop.get_f_value() < self.global_best_f_value:
                    self.global_best_values = pop.get_values()
                    self.global_best_f_value = pop.get_f_value()

    @abstractmethod
    def next_generation_generate(self,pops:List[State]):
        pass

    @abstractmethod
    def pops_evaluate(self,pops:List[State]):
        pass
