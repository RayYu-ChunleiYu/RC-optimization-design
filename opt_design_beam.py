from ConstrainGA import ConstrainGA
from ConstrainPSO import ConstrainPSO
import time

def target_func(b,h,A_g,cost_concrete=400/1000000,cost_steel=35000/1000000):
    return b*h*cost_concrete+cost_steel*A_g

def constrain_1_moment(b,h,A_g,a=45,fc=12.5,fy=310,gama_d=1.2,M=47.58*10**6):
    h_0 = h-a
    xi = fy*A_g/(fc*b*h_0)
    alpha_s = xi*(1-0.5*xi)
    return (fc*alpha_s*b*h_0*h_0)/gama_d-M

def constrain_2_rhi_min(b,h,A_g,a=45,rhi_min=0.15/100):
    h_0 = h-a
    rhi = A_g/b/h_0
    return rhi-rhi_min

def constrain_3_xi_b(b,h,A_g,a=45,fc=12.5,fy=310,xi_b=0.544):
    h_0 = h-a
    xi = fy*A_g/(fc*b*h_0)
    return xi_b-xi

def constrain_4_xi_d(b,h,A_g,a=45,fc=12.5,V=30000):
    h_0 = h-a
    return 0.07*fc*b*h_0-V

def constrain_5_b(b,h,A_g):
    return b-0

def constrain_6_h(b,h,A_g):
    return h-0

def constrain_6_b_min(b,h,A_g,b_0=200):
    return b-b_0

if __name__ == "__main__":
    
    
    t1 = time.time()
    # # GA
    boundary = [[200,400],[0,800],[400,800]]
    GA_params = {
        "pop_size":10000,
        "iteration_num":10,
        "mutation_prob_limit":0.05
    }
    CGA = ConstrainGA()
    CGA.set_boundary(boundary)
    CGA.set_algorithm_param(**GA_params)
    CGA.set_target_func(target_func)
    CGA.set_constraint_func([constrain_1_moment,constrain_2_rhi_min,constrain_3_xi_b,constrain_4_xi_d,constrain_5_b,constrain_6_h,constrain_6_b_min])
    CGA.run(multi_thread=True)


    # boundary = [[200,400],[0,800],[400,800]]
    # PSO_param = {
    #     "pop_size": 10000,
    #     "iteration_num": 10,
    #     "w": 0.3,
    #     "c1": 1.4,
    #     "c2": 1.4,
    # }
    # CPSO = ConstrainPSO()
    # CPSO.set_boundary(boundary)
    # CPSO.set_algorithm_param(**PSO_param)
    # CPSO.set_target_func(target_func)
    # CPSO.set_constraint_func([constrain_1_moment,constrain_2_rhi_min,constrain_3_xi_b,constrain_4_xi_d,constrain_5_b,constrain_6_h,constrain_6_b_min])
    # CPSO.run(multi_thread=True)
    t2 = time.time()
    print("time:",t2-t1)
