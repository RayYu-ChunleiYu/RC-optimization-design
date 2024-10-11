from ConstrainGA import ConstrainGA
from ConstrainPSO import ConstrainPSO

def target_func(b,h,A_g,cost_concrete=400/1000000,cost_steel=35000/1000000):
    return b*h*cost_concrete+cost_steel*A_g

def constrain_1_capacity(b,h,A_g,a=45,l=6500,fc=10,fy=310,gamma_d=1.2,N=651000):
    l_0 = l*0.7
    phi =1.2687-0.0291*l_0/b+0.0001*(l_0/b)**2
    A_c = (b-2*a)*(h-2*a)-A_g
    cal_N = (fc*A_c+fy*A_g)*phi/gamma_d
    return cal_N-N

def constrain_2_rhi_max(b,h,A_g,rhi_max=3.0/100):
    rhi = A_g/b/h
    return rhi_max-rhi

def constrain_3_rhi_min(b,h,A_g,rhi_min=0.4/100):
    rhi = A_g/b/h
    return rhi-rhi_min


def constrain_4_b(b,h,A_g):
    return b-0

def constrain_5_h(b,h,A_g):
    return h-0

def constrain_5_h(b,h,A_g):
    return h-0

def constrain_6_b_min(b,h,A_g,b_0=200):
    return b-b_0

if __name__ == "__main__":
    boundary = [[200,400],[0,800],[800,2000]]
    PSO_param = {
        "pop_size": 1000,
        "iteration_num": 10,
        "w": 0.3,
        "c1": 1.4,
        "c2": 1.4,
    }
    CPSO = ConstrainPSO()
    CPSO.set_boundary(boundary)
    CPSO.set_algorithm_param(**PSO_param)
    CPSO.set_target_func(target_func)
    CPSO.set_constraint_func([constrain_1_capacity,constrain_2_rhi_max,constrain_3_rhi_min,constrain_4_b,constrain_5_h,constrain_6_b_min])
    CPSO.run(multi_thread=True)

