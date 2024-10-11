import subprocess
from .InpGenerator import InpReplacer,GenFiber
import pandas as pd 
import numpy as np 
import os
import time
import random

class FiberModelRunner:
    def __init__(self,solver_path='fiberModel.exe') -> None:
        self.solver_path = solver_path

    def run(self,inp_model_file_path:str="model.inp",output_file = "results.csv",log_file = "log.txt"):
        command = f"{self.solver_path} -i {inp_model_file_path} -o {output_file} -l {log_file}"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

class PostProcessor:
    @classmethod    
    def get_peak_momentX(cls,output_file:str="results.csv"):
        data = pd.read_csv(output_file)
        force = data['section-5-momentX']
        return np.abs(force).max()


def steel_gap_fiber_hori(b,layer,gap,y_location,d):
    x_locations = []
    c_x_location = gap/2
    while c_x_location <= (b/2-layer-d/2):
        x_locations.append(c_x_location)
        c_x_location += gap
    x_locations_negative = [-x for x in x_locations]
    x_locations.extend(x_locations_negative)

    steel_x_location = x_locations
    steel_y_location = np.ones_like(steel_x_location)*y_location
    area = np.ones_like(steel_x_location)*(d/2)**2*np.pi
    steel_fiber_u = GenFiber.locate_fiber(steel_x_location,steel_y_location,area)
    return steel_fiber_u

def steel_gap_fiber_vert(h,gap,x_location,d):
    y_locations = []
    c_y_location = gap/2
    while c_y_location <= (h/2-d/2):
        y_locations.append(c_y_location)
        c_y_location += gap
    y_locations_negative = [-x for x in y_locations]
    y_locations.extend(y_locations_negative)

    steel_y_location = y_locations

    steel_x_location = np.ones_like(steel_y_location)*x_location
    area = np.ones_like(steel_x_location)*(d/2)**2*np.pi
    steel_fiber_u = GenFiber.locate_fiber(steel_x_location,steel_y_location,area)
    return steel_fiber_u


    

def all_factors(b1:float,b2:float,b3:float,h1:float,h2:float,h3:float,a:float,d_u:float,d_m:float,d_l:float,d_side:float,gap:float):
    concrete_fiber_1 = GenFiber.box(b2*2+b3,h1+h2+h3,[h1,h3,b2,b2],[3,4,2,2],[5,5,5,5])
    concrete_fiber_2 = GenFiber.rectangular(b1,h1,3,3,(-b3/2-b2-b1/2,h2/2+h3/2))
    concrete_fiber_3 = GenFiber.rectangular(b1,h1,3,3,(b3/2+b2+b1/2,h2/2+h3/2))
    concrete_fiber = GenFiber.concat_fibers(concrete_fiber_1,concrete_fiber_2,concrete_fiber_3)

    layer = 20

    steel_fiber_u = steel_gap_fiber_hori(b1*2+b2*2+b3,layer,gap,(h1+h2+h3)/2-layer-d_u/2,d_u)
    steel_fiber_m = steel_gap_fiber_hori(b1*2+b2*2+b3,layer,gap,(h1+h2+h3)/2-h1+layer+d_m/2,d_m)
    steel_fiber_l = steel_gap_fiber_hori(b3,layer,gap,-(h1+h2+h3)/2+layer+d_l/2,d_l)
    steel_fiber_s_1 = steel_gap_fiber_vert(h2,gap,-b3/2-b2+layer+d_side/2,d_side)
    steel_fiber_s_2 = steel_gap_fiber_vert(h2,gap,b3/2+b2-layer-d_side/2,d_side)
    steel_fiber_s = GenFiber.concat_fibers(steel_fiber_s_1,steel_fiber_s_2)
    steel_fiber_s = GenFiber.move_fiber_centre(steel_fiber_s,0,-(h1-h3)/2)
    steel_fiber = GenFiber.concat_fibers(steel_fiber_u,steel_fiber_m,steel_fiber_l,steel_fiber_s)
    all_fiber = GenFiber.concat_fibers(concrete_fiber,steel_fiber)

    h2 = int(h2)
    d_u = int(d_u)
    gap = int(gap)
    model_name_base = f"model_{h2}_{d_u}_{gap}"
    index = 1
    model_name = f"{model_name_base}_{index}"
    while os.path.exists(os.path.join("FiberModelOpt","cache",f'{model_name}.inp')):
        index += 1
        model_name = f"{model_name_base}_{index}"
    ING = InpReplacer(os.path.join("FiberModelOpt","model_template.inp"))
    ING.fiber_replace([concrete_fiber,steel_fiber],[1,2],[1,1])
    output_model_input =os.path.join('FiberModelOpt',"cache", f'{model_name}.inp')
    ING.write_inp(output_model_input)
    FMR = FiberModelRunner(os.path.join("FiberModelOpt","fiberModel.exe"))
    results_file=os.path.join("FiberModelOpt","cache", f'{model_name}.csv')
    pic_file=os.path.join("FiberModelOpt","cache", f'{model_name}.png')
    log_file=os.path.join("FiberModelOpt","cache", f'{model_name}.log')
    # GenFiber.plot_fibers(all_fiber,pic_file)
    FMR.run(output_model_input,results_file,log_file)
    # time.sleep(0.)
    # try:
    peak_moment = PostProcessor.get_peak_momentX(results_file)
    # except KeyError:
    #     print(results_file)
    #     peak_moment = 0
    # except pd.errors.EmptyDataError:
    #     print(results_file)
    #     peak_moment = 0
    # finally:
    #     pass
    

    # self-weight load summary
    concrete_area = 0
    for fiber in concrete_fiber['area']:
        concrete_area += fiber
    steel_area = 0
    for fiber in steel_fiber['area']:
        steel_area += fiber
    steel_density = 7850
    concrete_density = 2500
    q_steel = steel_area*steel_density/1000000*10/1000
    q_concrete = concrete_area*concrete_density/1000000*10/1000

    return peak_moment,q_steel+q_concrete

def all_factors_area(b1:float,b2:float,b3:float,h1:float,h2:float,h3:float,a:float,d_u:float,d_m:float,d_l:float,d_side:float,gap:float):
    concrete_fiber_1 = GenFiber.box(b2*2+b3,h1+h2+h3,[h1,h3,b2,b2],[3,4,2,2],[5,5,5,5])
    concrete_fiber_2 = GenFiber.rectangular(b1,h1,3,3,(-b3/2-b2-b1/2,h2/2+h3/2))
    concrete_fiber_3 = GenFiber.rectangular(b1,h1,3,3,(b3/2+b2+b1/2,h2/2+h3/2))
    concrete_fiber = GenFiber.concat_fibers(concrete_fiber_1,concrete_fiber_2,concrete_fiber_3)

    layer = 20

    steel_fiber_u = steel_gap_fiber_hori(b1*2+b2*2+b3,layer,gap,(h1+h2+h3)/2-layer-d_u/2,d_u)
    steel_fiber_m = steel_gap_fiber_hori(b1*2+b2*2+b3,layer,gap,(h1+h2+h3)/2-h1+layer+d_m/2,d_m)
    steel_fiber_l = steel_gap_fiber_hori(b3,layer,gap,-(h1+h2+h3)/2+layer+d_l/2,d_l)
    steel_fiber_s_1 = steel_gap_fiber_vert(h2,gap,-b3/2-b2+layer+d_side/2,d_side)
    steel_fiber_s_2 = steel_gap_fiber_vert(h2,gap,b3/2+b2-layer-d_side/2,d_side)
    steel_fiber_s = GenFiber.concat_fibers(steel_fiber_s_1,steel_fiber_s_2)
    steel_fiber_s = GenFiber.move_fiber_centre(steel_fiber_s,0,-(h1-h3)/2)
    steel_fiber = GenFiber.concat_fibers(steel_fiber_u,steel_fiber_m,steel_fiber_l,steel_fiber_s)

    # self-weight load summary
    concrete_area = 0
    for fiber in concrete_fiber['area']:
        concrete_area += fiber
    steel_area = 0
    for fiber in steel_fiber['area']:
        steel_area += fiber

    return concrete_area,steel_area



def design_factors_load_and_resistenace(h2,gap,d):
    return all_factors(500,100,1000,300,h2,100,5,d,d,d,d,gap)

def design_factors_area(h2,gap,d):
    return all_factors_area(500,100,1000,300,h2,100,5,d,d,d,d,gap)




if __name__ == "__main__":
    # # ING = InpReplacer("model_template.inp")
    # # ING.fiber_replace("circle",d=168,t=8)
    # # output_model_input = 'model_1.inp'
    # # ING.write_inp(output_model_input)
    # # FMR = FiberModelRunner()
    # # FMR.run(output_model_input,"model_1_results.csv")
    # print(all_factors(500,100,1000,300,500,100,5,16,16,16,16,100))
    # print(design_factors_load_and_resistenace(500,100,20))
    pass
