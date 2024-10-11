import matplotlib.pyplot as plt
import numpy as np 
from typing import Tuple,Union,List

class InpReplacer:
    def __init__(self,inp_model_file_path:str="model_template.inp") -> None:
        self.inp_model_file_path = inp_model_file_path
        with open(self.inp_model_file_path,'r') as f:
            model_inp = f.readlines()
            model_inp  = [line.rstrip() for line in model_inp]
        self.inp_model_content = model_inp
    
    def section_delete(self,section_str:str):
        if section_str.lower() in ['fiber','material']:
            fiber_start_index = self.inp_model_content.index(f"#{section_str.capitalize()}")
            fiber_end_index = self.inp_model_content.index(f"#End{section_str.capitalize()}")
            # delete old fibers
            del self.inp_model_content[fiber_start_index+1:fiber_end_index]
        else:
            raise ValueError("Wrong section name")
        return self

    def fiber_replace(self,fibers:Union[List[dict],dict],material_num:Union[List[int],int],section_num:Union[List[int],int]):
        if isinstance(fibers,dict):
            fibers = [fibers]
        if isinstance(material_num,int):
            material_num = [material_num]
        if isinstance(section_num,int):
            section_num = [section_num]

        section_label = "Fiber"
        self.section_delete(section_label)
        fiber_start_index = self.inp_model_content.index(f"#{section_label.capitalize()}")

        new_fibers = []
        for fiber_dict,material_id,section_id in zip(fibers,material_num,section_num):
            for i in range(len(fiber_dict['location_x'])):
                new_fibers.append(f"{fiber_dict['location_x'][i]} {fiber_dict['location_y'][i]} {fiber_dict['area'][i]} {material_id} {section_id}")
        for i,fiber in enumerate(new_fibers):
            self.inp_model_content.insert(fiber_start_index+1+i,f"{i+1} {fiber}")
        return self
    
    def material_replace(self,materials_name,materials_id:Union[List[int],int],materials_param:Union[List[List],List]):
        if isinstance(materials_name,str):
            materials_name = [materials_name]
        if isinstance(materials_id,int):
            materials_id = [materials_id]
        if not isinstance(materials_param[0],List):
            materials_param = [materials_param]
        section_label = "Material"
        self.section_delete(section_label)
        material_start_index = self.inp_model_content.index(f"#{section_label.capitalize()}")

        j=0
        for material_name,material_id,material_param in zip(materials_name,materials_id,materials_param):
            material_param = " ".join([str(i) for i in material_param])
            self.inp_model_content.insert(material_start_index+1+j,f"{material_name} {material_id} {material_param}")
            j += 1
        return self
    
    def record_replace(self,records_id:Union[List[int],int],records_type:Union[List[str],str],records_target_id:Union[List[int],int],records_target:Union[List[str],str]):
        if isinstance(records_id,int):
            records_id = [records_id]
        if isinstance(records_type,str):
            records_type = [records_type]
        if isinstance(records_target_id,int):
            records_target_id = [records_target_id]
        if isinstance(records_target,str):
            records_target = [records_target]

        section_label = "Record"
        self.section_delete(section_label)
        record_start_index = self.inp_model_content.index(f"#{section_label.capitalize()}")
        j=0
        for record_id,record_type,record_target_id,record_target in zip(records_id,records_type,records_target_id,records_target):
            self.inp_model_content.insert(record_start_index+1+j,f"{record_id} {record_type} {record_target_id} {record_target}")
            j += 1
        return self

    def write_inp(self,inp_model_file_path:str="model.inp"):
        with open(inp_model_file_path,'w') as f:
            for line in self.inp_model_content:
                f.write(line)
                f.write("\n")
        return self
    

class GenFiber(object):
    @staticmethod

    def locate_fiber(location_x:Union[List[float],float],location_y:Union[List[float],float],area:Union[List[float],float])->dict:
        if isinstance(location_x,float):
            location_x = [location_x]
        if isinstance(location_y,float):
            location_y = [location_y]
        if isinstance(area,float):
            area = [area]
        #check the length
        if len(location_x) != len(location_y):
            raise ValueError("The length of location_x and location_y should be equal")
        if len(location_x) != len(area):
            raise ValueError("The length of location_x and area should be equal")
        
        return {
            "location_x":location_x,
            "location_y":location_y,
            "area":area
        }
    
    def concat_fibers(*fibers)->dict:
        fiber_info = {
            "location_x":[],
            "location_y":[],
            "area":[]
        }
        for fiber in fibers:
            if isinstance(fiber,dict):
                [fiber_info['location_x'].append(i) for i in fiber['location_x']]
                [fiber_info['location_y'].append(i) for i in fiber['location_y']]
                [fiber_info['area'].append(i) for i in fiber['area']]
            else:
                raise ValueError("Wrong type for fibers info")
        return fiber_info

    @staticmethod
    def move_fiber_centre(fiber_info:dict,move_x:float,move_y:float)->dict:
        for i in range(len(fiber_info['location_x'])):
            fiber_info['location_x'][i] += move_x
            fiber_info['location_y'][i] += move_y
        return fiber_info

    @staticmethod
    def plot_fibers(fiber_info:dict,pic_path:str)->None:
        locx = []
        locy = []
        area = []

        for i in range(len(fiber_info['location_x'])):
            locx.append(fiber_info['location_x'][i])
            locy.append(fiber_info['location_y'][i])
            area.append(fiber_info['area'][i])
        size_adjust = 1/100
        area = [i*size_adjust for i in area]

        plt.cla()
        fig, ax = plt.subplots()
        ax.scatter(locx, locy, s=area,color='blue')
        ax.set_aspect('equal', adjustable='box')
        plt.savefig(pic_path)

    @staticmethod
    def outputToFile(fibers_info:dict,filepath:str,addition_string:str = ""):
        content = []
        for i,_ in enumerate(fibers_info['location_x']):
            line = f"{i+1} {fibers_info['location_x'][i]} {fibers_info['location_y'][i]} {fibers_info['area'][i]} {addition_string}\n"
            content.append(line)
        with open(filepath,'w') as f:
            f.writelines(content)
    
    @staticmethod
    def circle(diameter:float,r_dimension:int,theta_dimension:int,location_center:Tuple[float]=(0,0))->dict:
        fiber_info = {
            "location_x":[],
            "location_y":[],
            "area":[]
        }
        radius = diameter/2
        r_direction_gap =  radius/ r_dimension
        r_direction_value_list = [
            r_direction_gap * (i + 0.5) for i in range(1, r_dimension)
        ]
        theta_direction_gap = 360 / theta_dimension
        theta_direction_value_list = [
            theta_direction_gap * i for i in range(theta_dimension)
        ]
        for i in r_direction_value_list:
            for j in theta_direction_value_list:
                fiber_info["location_x"].append(
                    i * np.cos(j / 360 * 2 * np.pi)+location_center[0]
                )
                fiber_info["location_y"].append(
                    i * np.sin(j / 360 * 2 * np.pi)+location_center[1]
                )
                fiber_info["area"].append(
                    i * theta_direction_gap / 360 * 2 * np.pi * r_direction_gap
                )
        fiber_info["location_x"].append(0+location_center[0])
        fiber_info["location_y"].append(0+location_center[1])
        fiber_info["area"].append(np.pi * r_direction_gap ** 2)

        return fiber_info

    @staticmethod
    def ring(diameter:float,thickness:int,r_dimension:int,theta_dimension:int,location_center:Tuple[float]=(0,0))->dict:
        fiber_info = {
            "location_x":[],
            "location_y":[],
            "area":[]
        }
        radius = diameter/2
        r_direction_gap =  thickness/ r_dimension
        r_direction_value_list = [
            j + radius-thickness
            for j in [
                r_direction_gap * (i + 0.5) for i in range(0, r_dimension)
            ]
        ]

        theta_direction_gap = 360 / theta_dimension
        theta_direction_value_list = [
            theta_direction_gap * i for i in range(theta_dimension)
        ]
        for i in r_direction_value_list:
            for j in theta_direction_value_list:
                fiber_info["location_x"].append(
                    i * np.cos(j / 360 * 2 * np.pi)+location_center[0]
                )
                fiber_info["location_y"].append(
                    i * np.sin(j / 360 * 2 * np.pi)+location_center[1]
                )
                fiber_info["area"].append(
                    i * theta_direction_gap / 360 * 2 * np.pi * r_direction_gap
                )

        return fiber_info
    @staticmethod
    def rectangular(width:float,height:float,width_dimension:int,height_dimension:int,location_center:Tuple[float]=(0,0))->dict:
        """width -> direction x    \n height -> direction y"""
        fiber_info = {
            "location_x":[],
            "location_y":[],
            "area":[]
        }
        x_left_value = -width / 2
        x_gap = abs(x_left_value) * 2 / width_dimension
        x_location_list = np.linspace(
            x_left_value + x_gap / 2, -x_left_value - x_gap / 2, width_dimension
        )
        y_down_value = -height / 2
        y_gap = abs(y_down_value) * 2 / height_dimension
        y_location_list = np.linspace(
            y_down_value + y_gap / 2, -y_down_value - y_gap / 2, height_dimension
        )
        area = x_gap * y_gap
        for i in x_location_list:
            for j in y_location_list:
                fiber_info["location_x"].append(i+location_center[0])
                fiber_info["location_y"].append(j+location_center[1])
                fiber_info["area"].append(area)
        return fiber_info
        
    @staticmethod
    def box(width:float,height:float,thickness:Union[float,list[float]],dimension_t:Union[int,list[int]],dimension_l:Union[int,list[int]],location_center:Tuple[float]=(0,0))->dict:
        ### thickness up down left and right 
        if isinstance(thickness,float):
            thickness = [thickness,thickness,thickness,thickness]
        elif isinstance(thickness,list):
            if len(thickness) == 2:
                thickness = [thickness[0],thickness[0],thickness[1],thickness[1]]
            elif len(thickness) ==4:
                pass
            else:
                raise ValueError("Wrong type for thcikness")
        else:
            raise ValueError("Wrong type for thcikness")
        
        if isinstance(dimension_t,int):
            dimension_t = [dimension_t,dimension_t,dimension_t,dimension_t]
        elif isinstance(dimension_t,list):
            if len(dimension_t) == 2:
                dimension_t = [dimension_t[0],dimension_t[0],dimension_t[1],dimension_t[1]]
            elif len(dimension_t)==4:
                pass
            else:
                raise ValueError("Wrong type for dimension_t")
        else:
            raise ValueError("Wrong type for dimentsion_t")

        if isinstance(dimension_l,int):
            dimension_l = [dimension_l,dimension_l,dimension_l,dimension_l]
        elif isinstance(dimension_l,list):
            if len(dimension_l) == 2:
                dimension_l = [dimension_l[0],dimension_l[0],dimension_l[1],dimension_l[1]]
            elif len(dimension_l)==4:
                pass
            else:
                raise ValueError("Wrong type for dimension_t")
        else:
            raise ValueError("Wrong type for dimentsion_t")
        
        #left 
        left_center_location = (-width/2+thickness[2]/2,0)
        left_fibers = GenFiber.rectangular(thickness[2],height,dimension_t[2],dimension_l[2],left_center_location)
        right_center_location = (width/2-thickness[3]/2,0)
        right_fibers = GenFiber.rectangular(thickness[3],height,dimension_t[3],dimension_l[3],right_center_location)
        top_center_location = (0,height/2-thickness[0]/2)
        top_fibers = GenFiber.rectangular(width-thickness[2]-thickness[3],thickness[0],dimension_l[0],dimension_t[0],top_center_location)
        bottom_center_location = (0,-height/2+thickness[1]/2)
        bottom_fibers = GenFiber.rectangular(width-thickness[2]-thickness[3],thickness[1],dimension_l[1],dimension_t[1],bottom_center_location)

        all_fibers = GenFiber.concat_fibers(left_fibers,right_fibers,top_fibers,bottom_fibers)
        moved_fibers = GenFiber.move_fiber_centre(all_fibers,location_center[0],location_center[1])
        return moved_fibers


if __name__ == "__main__":
    # SectionInputGenerator.circle_plot(200,10,1,2,1,10,10)
    # fibers = GenFiber.box(1000,200,10.0,3,10)
    # fibers = GenFiber.circle(100,10,10)
    # fibers = GenFiber.ring(100,20,3,10)
    # fibers = GenFiber.rectangular(100,100,10,10)

    fibers = GenFiber.ring(168,10,2,10)
    fibers_rec = GenFiber.rectangular(100,100,10,10)
    fibers_all = GenFiber.concat_fibers(fibers,fibers_rec)
    GenFiber.plot_fibers(fibers_all)

    # InpReplacer().fiber_replace(fibers_all,1,1).material_replace('a',1,[1.0,1000,1.0000,1]).write_inp()
    # InpReplacer().fiber_replace(fibers_all,1,1).material_replace(['a','b'],[1,2],[[1.0,1000,1.0000,1],[1.0,1000,1.0000,1]]).write_inp()

    # inpGen = InpGenerator("model.inp")
    # inpGen.fiber_replace("circle",d=200,t=10)
    # inpGen.write_inp()

