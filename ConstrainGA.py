import numpy as np 
from typing import List
import copy
import random
from State import State
from ConstrainAlg import ConstrainAlg

class ConstrainGA(ConstrainAlg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mutation(self,pop_1:State,mutation_prob_limit:float=0.05):

        x = copy.deepcopy(pop_1.get_values())
        n = x.shape[0]
        mutation_prob = np.random.rand(n)
        x_need_mutate = x[mutation_prob < mutation_prob_limit]
        x_need_mutate= x_need_mutate + np.random.randn(x_need_mutate.shape[0])
        x[mutation_prob < mutation_prob_limit] = x_need_mutate
        pop_1.update_value(x)

    def crossover(self,pop_1:State,pop_2:State):
        x_1:np.ndarray = pop_1.get_values()
        x_2:np.ndarray = pop_2.get_values()
        n = x_1.shape[0];
        pos = np.random.randint(0,n-1); 
        x_1[pos],x_2[pos] = x_2[pos],x_1[pos]
        pop_1.update_value(x_1)
        pop_2.update_value(x_2)

    def tournament_selection(self,pops:List[State],K, N, *fitness_values):
        """
        Tournament selection function to select N individuals based on their fitness values.
        
        Parameters:
        K (int): Number of individuals participating in each tournament.
        N (int): Number of individuals to select.
        fitness_values (tuple of np.ndarray): Tuple of fitness values for each individual.
        
        Returns:
        np.ndarray: Indices of the selected individuals.
        """
        # Ensure all fitness values are column vectors
        constrain_breaks = np.zeros(len(pops))
        f_values = np.zeros(len(pops))
        for i,pop in enumerate(pops):
            constrain_breaks[i] = pop.get_constrain_break()
            f_values[i] = pop.get_f_value()
        fitness_values = tuple([constrain_breaks,f_values])
        fitness_values = [np.reshape(fitness, (-1, 1)) for fitness in fitness_values]
        
        # Combine fitness values into a single array
        combined_fitness = np.hstack(fitness_values)
        
        # Sort individuals based on combined fitness values
        sorted_indices = np.lexsort(combined_fitness.T[::-1])
        
        # Create a rank vector based on sorted indices
        rank = np.empty_like(sorted_indices)
        rank[sorted_indices] = np.arange(len(sorted_indices))
        
        # Select parents using tournament selection
        selected_indices = []
        for _ in range(N):
            # Randomly select K individuals
            candidates = random.sample(range(len(rank)), K)
            # Find the best candidate based on rank
            best_candidate = min(candidates, key=lambda x: rank[x])
            selected_indices.append(best_candidate)
        selected_pops = [copy.deepcopy(pops[i]) for i in selected_indices]
        return selected_pops

    def pops_evaluate(self,pop:State):
        values = pop.get_values()
        pop.update_f_value(self.target_func(*values))
        constrain_break = 0
        for constrain_func in self.constrain_funcs:
            if constrain_func(*values) < 0:
                constrain_break += 1
        pop.update_constrain_break(constrain_break)

    def next_generation_generate(self,pops:List[State]):
        mutation_prob_limit = self.algorithm_param["mutation_prob_limit"]
        next_gen = []
        for i in range(0,int(np.floor(len(pops)/2))):
            pop_1 = pops[2*i]
            pop_2 = pops[2*i+1]
            pop_1_next_gen = copy.deepcopy(pop_1)
            pop_2_next_gen = copy.deepcopy(pop_2)
            self.crossover(pop_1_next_gen,pop_2_next_gen)
            self.mutation(pop_1_next_gen,mutation_prob_limit)
            self.mutation(pop_2_next_gen,mutation_prob_limit)
            self.bounds_constrain(pop_1_next_gen)
            self.bounds_constrain(pop_2_next_gen)
            next_gen.append(pop_1_next_gen)
            next_gen.append(pop_2_next_gen)
        next_gen = self.tournament_selection(next_gen,2,len(next_gen))
        return next_gen

if __name__ == "__main__":
    boundary = [[0,1],[2,3]]
    target_func = lambda x1,x2:(x1-0.8)**2+(x2-2.5)**2
    constrain_func_1 = lambda x1,x2:x1-0.9
    CGA= ConstrainGA()
    CGA.set_boundary(boundary)
    CGA.set_target_func(target_func)
    CGA.set_constraint_func(constrain_func_1)
    GA_params = {
        "pop_size":100,
        "iteration_num":100,
        "mutation_prob_limit":0.05
    }
    CGA.set_algorithm_param(**GA_params)
    CGA.run()