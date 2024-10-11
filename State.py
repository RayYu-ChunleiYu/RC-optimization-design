import numpy as np 
from typing import List
import copy

class State:

    def __init__(self,boundaries:List[List[float]],values=None,constrain_break=None,f_value=None,extra_info=None) -> None:
        self.boundaries = boundaries
        if values is not None:
            self.values = values
        else:
            self.bounds_lower = np.array([i[0] for i in boundaries])
            self.bounds_gap = np.array([i[1]-i[0] for i in boundaries])
            num_values = len(boundaries)
            self.values = np.random.rand(num_values)*self.bounds_gap+self.bounds_lower
        if constrain_break is not None:
            self.constrain_break = constrain_break
        else:
            self.constrain_break = 0
        if f_value is not None:
            self.f_value = f_value
        else:
            self.f_value = 0
        
        if extra_info is not None:
            self.extra_info = extra_info
        else:
            self.extra_info = {}

    def update_f_value(self,f_value:float):
        self.f_value = f_value

    def update_value(self,values:np.ndarray):
        self.values = values

    def update_constrain_break(self,constrain_break:int):
        self.constrain_break = constrain_break

    def update_extra_info(self,extra_info):
        self.extra_info = extra_info
    
    def get_extra_info(self):
        return self.extra_info

    def get_values(self):
        return self.values
    
    def get_f_value(self):
        return self.f_value

    def get_constrain_break(self):
        return self.constrain_break

    def __deepcopy__(self, memo):
        values = copy.deepcopy(self.values,memo)
        constrain_break = copy.deepcopy(self.constrain_break,memo)
        f_value = copy.deepcopy(self.f_value,memo)
        return State(self.boundaries,values,constrain_break,f_value)

    def __repr__(self) -> str:
        return f"{self.values}  -> {self.f_value} with {self.constrain_break} constrain break"



