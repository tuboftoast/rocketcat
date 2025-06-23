from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import numpy as np 
import matplotlib.pyplot as plt
import time
import math
import pandas as pd
import csv
import os
import RocketFunctions2
from RocketFunctions2 import nozzle_geometry


# global variable for folder path, make sure there is a \\ at the end of it
Folder_Path = "C:\\Users\\joesb\\CSVFiles"

#Configuration Class
class Config:

    def __init__(self,input_params,input_name):

        self.input_params = input_params
        self.input_name = input_name

    def process_data(self):
        
        input_params = self.input_params
        input_name = self.input_name

        #Creates CSV file that stores data into a file.
        CSVWriter(input_params,input_name).createfile()

#CSV Writer class
class CSVWriter:
    def __init__(self,input_params,input_name):
        
        self.input_params = input_params
        self.input_name = input_name

    def createfile(self):

        self.input_gamma = self.input_params[0]
        self.input_R = self.input_params[1]
        self.input_P0 = self.input_params[2]
        self.input_T0 = self.input_params[3]
        self.input_Mdot = self.input_params[4]
        self.input_Din = self.input_params[5]
        self.input_Dthroat = self.input_params[6]
        self.input_Dexit = self.input_params[7]
        self.input_xthroat = self.input_params[8]
        self.input_xexit = self.input_params[9]
        self.input_name = self.input_name
 

        data = {'Gamma':[self.input_gamma],'R':[self.input_R],'P0':[self.input_P0],'T0':[self.input_T0],'Mdot':[self.input_Mdot],'Din':[self.input_Din],'Dthroat':[self.input_Dthroat],'Dexit':[self.input_Dexit],'xthroat':[self.input_xthroat],'xexit':[self.input_xexit],'name':[self.input_name]}
        df = pd.DataFrame(data)

        #File path
        file_path = Folder_Path + self.input_name

        df.to_csv(file_path,index=False)

#configuration manager
class ConfigManager:
    def __init__(self,folder_path):

        self.folder_path = Folder_Path
    
    def obtain_config_list(self):

        folder_path = Folder_Path

        config_list = os.listdir(folder_path)
        self.config_list = config_list

        print(config_list)

        return config_list


#Home Screen
class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        #Initializing layout
        home_layout = FloatLayout()
        self.home_layout = home_layout
        self.add_widget(home_layout)

        #Nav Buttons
        input_button = Button(text='Input',on_press=self.switch_to_second,size_hint=(0.3,0.1),pos_hint={'center_x':0.1,'center_y':0.05})
        home_layout.add_widget(input_button)

        config_button = Button(text='Configurations',on_press=self.switch_to_third,size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.05})
        home_layout.add_widget(config_button)

        #Labels 
        rocketcatlogo = Image(source='logo.png',allow_stretch=True,keep_ratio=True,size_hint=(0.5,0.5),pos_hint={'center_x':0.5,'center_y':0.6})
        home_layout.add_widget(rocketcatlogo)
        home_page_title = Label(text='Welcome to RocketCat!',size_hint=(10,10),pos_hint={'center_x':0.5,'center_y':0.3})
        home_layout.add_widget(home_page_title)

    def switch_to_third(self,instance):
        self.manager.current = 'third'
    def switch_to_second(self, instance):
        self.manager.current = 'second'

#Input Screen
class InputScreen(Screen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)

        #Initializing layout
        input_layout = FloatLayout()
        self.input_layout = input_layout
        self.add_widget(input_layout)

        #bg_image = Image(source='bgimage.png',allow_stretch=True,keep_ratio=False)
        #input_layout.add_widget(bg_image)

        self.input_gamma = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.2,'center_y':0.95},hint_text='Enter Gamma Value (Cv/Cp)'))
        input_layout.add_widget(self.input_gamma)
        self.input_R = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.2,'center_y':0.85},hint_text='Enter Specific Gas Constant (J/kg*k)'))
        input_layout.add_widget(self.input_R)
        self.input_P0 = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.2,'center_y':0.75},hint_text='Enter Combustion Chamber Pressure (Pa)'))
        input_layout.add_widget(self.input_P0)
        self.input_T0 = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.2,'center_y':0.65},hint_text='Enter Combustion Chamber Temperature (K)'))
        input_layout.add_widget(self.input_T0)
        self.input_Mdot = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.5,'center_y':0.3},hint_text='Enter Mass Flow Rate (kg/sec)'))
        input_layout.add_widget(self.input_Mdot)

        self.input_Din = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.8,'center_y':0.95},hint_text='Enter inlet diameter (m)'))
        input_layout.add_widget(self.input_Din)
        self.input_Dthroat = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.8,'center_y':0.85},hint_text='Enter throat diameter (m)'))
        input_layout.add_widget(self.input_Dthroat)
        self.input_Dexit = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.8,'center_y':0.75},hint_text='Enter exit diameter (m)'))
        input_layout.add_widget(self.input_Dexit)
        self.input_xthroat = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.8,'center_y':0.65},hint_text='Enter throat distance (m)'))
        input_layout.add_widget(self.input_xthroat)
        self.input_xexit = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.8,'center_y':0.55},hint_text='Enter exit distance (m)'))
        input_layout.add_widget(self.input_xexit)


        self.input_name = (TextInput(multiline=False,size_hint=(0.4,0.1),pos_hint={'center_x':0.2,'center_y':0.55},hint_text='Enter Config. Name'))
        input_layout.add_widget(self.input_name)

        self.home_button1 = Button(text='Home',on_press=self.switch_to_home,size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.05})

        submit_button = Button(text='Save Configuration',on_press=self.on_submit,size_hint=(0.3,0.1),pos_hint={'center_x':0.5,'center_y':0.1})
        self.submit_button = submit_button

        input_layout.add_widget(self.home_button1)

        input_layout.add_widget(self.submit_button)

    def on_submit(self,instance):

        #input parameters vector
        input_params = np.zeros(10)
        input_params[0] = float(self.input_gamma.text)
        input_params[1] = float(self.input_R.text)
        input_params[2] = float(self.input_P0.text)
        input_params[3] = float(self.input_T0.text)
        input_params[4] = float(self.input_Mdot.text)
        input_params[5] = float(self.input_Din.text)
        input_params[6] = float(self.input_Dthroat.text)
        input_params[7] = float(self.input_Dexit.text)
        input_params[8] = float(self.input_xthroat.text)
        input_params[9] = float(self.input_xexit.text)
        input_name = self.input_name.text

        Config(input_params,input_name).process_data()


    def switch_to_home(self, instance):
        self.manager.current = 'home' 


#Configurations Screen
class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)

        #initializing layout
        config_layout = FloatLayout()
        self.config_layout = config_layout
        self.add_widget(config_layout)

        config_list_layout = FloatLayout()
        self.config_list_layout = config_list_layout
        self.add_widget(config_list_layout)

        #bg_image = Image(source='bgimage.png',allow_stretch=True,keep_ratio=False)
        #config_layout.add_widget(bg_image)

        self.home_button1 = Button(text='Home',on_press=self.switch_to_home,size_hint=(0.3,0.1),pos_hint={'center_x':0.1,'center_y':0.05})
        config_layout.add_widget(self.home_button1)

        self.test_button = Button(text='Update',on_press=self.update_config_list,size_hint=(0.3,0.1),pos_hint={'center_x':0.5,'center_y':0.05})
        config_layout.add_widget(self.test_button)

        #when this function is called, it will update the displayed configurations list.
    def update_config_list(self,Folder_path):

        config_list_layout = self.config_list_layout
        config_list_layout.clear_widgets()

        folder_path = Folder_path

        #temp variables
        button_num = 0
        index = 0
        y_val = 0.6

        config_list = ConfigManager(folder_path).obtain_config_list()
         # For loop for creating buttons that coorespond to the files.

        for config in config_list:
            
            #self.remove_widget(equation_list_layout)
            
            button_name = f"button_{button_num}"
            button_name_indexed = config_list[index]

            file_name = Folder_Path + f'\\{config_list[index]}'

            button_name= Button(text=button_name_indexed,on_press=lambda instance, file=file_name: self.open_file(file) , size_hint=(0.3,0.1), pos_hint={'center_x':0.5,'center_y':y_val})

            config_list_layout.add_widget(button_name)

            print(file_name)

            #looping variables
            button_num += 1
            index += 1
            y_val = y_val - 0.1

        #for some reason this didnt work before, but now it do!!!!!!!!!!!!!!!!!!!!! :)
        self.remove_widget(config_list_layout)
        self.add_widget(config_list_layout)



    def open_file(self,file_name):

        df = pd.read_csv(file_name)
        print(file_name)

        #Calls for the creation of the note screen page passed with the desired file name
        config_page = ConfigPage(file_name=file_name, name='equation')
        config_page.create_config_page(file_name)
        self.manager.add_widget(config_page)

        #ABSOLUTE NECESITY FOR PASSING FILE_NAME!!!!!!!
        config_page = ConfigPage(file_name)
        config_page.create_config_page(file_name)
        #EXTREMELY IMPORTANT FOR PASSING NAME!!!!! DONT FUCK WITH!!!!

        self.manager.current = 'equation'

        return file_name
        

    def switch_to_home(self, instance):
        self.manager.current = 'home' 


#individual configuration screen
class ConfigPage(Screen):
    def __init__(self, file_name='', **kwargs):
        super(ConfigPage, self).__init__(**kwargs)
        config_page_layout = FloatLayout()
        self.add_widget(config_page_layout)

        self.config_page_layout = config_page_layout

    def create_config_page(self,file_name):

        df = pd.read_csv(file_name)
        
        gamma = float(df.iloc[0,0])
        R = float(df.iloc[0,1])
        P0 = float(df.iloc[0,2])
        T0 = float(df.iloc[0,3])
        Mdot = float(df.iloc[0,4])
        Din = float(df.iloc[0,5])
        Dthroat = float(df.iloc[0,6])
        Dexit = float(df.iloc[0,7])
        xthroat = float(df.iloc[0,8])
        xexit = float(df.iloc[0,9])
        config_name = str(df.iloc[0,10])

        self.gamma = gamma
        self.R = R
        self.P0 = P0
        self.T0 = T0
        self.Mdot = Mdot
        self.Din = Din
        self.Dthroat = Dthroat
        self.Dexit = Dexit
        self.xthroat = xthroat
        self.xexit = xexit


        config_name_label = Label(text=config_name,size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.95})
        self.config_page_layout.add_widget(config_name_label)

        gamma_label = Label(text='Gamma: '+str(gamma),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.90})
        self.config_page_layout.add_widget(gamma_label)

        R_label = Label(text='R: '+str(R),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.85})
        self.config_page_layout.add_widget(R_label)

        P0_label = Label(text='P0: '+str(P0),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.80})
        self.config_page_layout.add_widget(P0_label)

        T0_label = Label(text='T0: '+str(T0),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.75})
        self.config_page_layout.add_widget(T0_label)

        Mdot_label = Label(text='Mdot: '+str(Mdot),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.70})
        self.config_page_layout.add_widget(Mdot_label)

        Din_label = Label(text='Din: '+str(Din),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.65})
        self.config_page_layout.add_widget(Din_label)

        Dthroat_label = Label(text='Dthroat: '+str(Dthroat),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.6})
        self.config_page_layout.add_widget(Dthroat_label)

        Dexit_label = Label(text='Dexit: '+str(Dexit),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.55})
        self.config_page_layout.add_widget(Dexit_label)

        xthroat_label = Label(text='xthroat: '+str(xthroat),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.5})
        self.config_page_layout.add_widget(xthroat_label)
        
        xexit_label = Label(text='xexit: '+str(xexit),size_hint=(0.3,0.1),pos_hint={'center_x':0.9,'center_y':0.45})
        self.config_page_layout.add_widget(xexit_label)

        #back to notescreen button
        back_to_config_screen_button = Button(text='Back to Configurations',on_press = self.back_to_notescreen,size_hint=(0.3,0.1),pos_hint={'center_x':0.1,'center_y':0.05})
        self.config_page_layout.add_widget(back_to_config_screen_button)

        x = np.linspace(0, xexit, 200)
        nozzle_geo_button = Button(text='Display Geometry',on_press = lambda instance: self.display_geo(x,self.xthroat,self.xexit,self.Din,self.Dexit,self.Dthroat),size_hint=(0.3,0.1),pos_hint={'center_x':0.1,'center_y':0.7})
        self.config_page_layout.add_widget(nozzle_geo_button)

        mach_plot_button = Button(text='Display Mach Number Plot',on_press = lambda instance: self.display_mach(x,xthroat,xexit,Din,Dexit,Dthroat,gamma,Mdot,P0,T0,R),size_hint=(0.3,0.1),pos_hint={'center_x':0.1,'center_y':0.5})
        self.config_page_layout.add_widget(mach_plot_button)


    def display_geo(self,x,xthroat,xexit,Din,Dexit,Dthroat):

        nozzle_rad = RocketFunctions2.nozzle_geometry(x,xthroat,xexit,Din,Dexit,Dthroat)

        plt.figure(1,figsize=(12, 6))
        plt.plot(x, nozzle_rad, 'k-', linewidth=2)  # Top boundary
        plt.plot(x, -nozzle_rad, 'k-', linewidth=2)  # Bottom boundary
        plt.xlabel("Axial Position (m)")
        plt.ylabel("Radial Position (m)")
        plt.title('Mach Number Plot')
        plt.show()

    def display_mach(self,x,xthroat,xexit,Din,Dexit,Dthroat,gamma,Mdot,P0,T0,R):

        nozzle_rad = RocketFunctions2.nozzle_geometry(x,xthroat,xexit,Din,Dexit,Dthroat)

        mach_vec = RocketFunctions2.Mach_Vector(RocketFunctions2.Mach_Equation,gamma,nozzle_rad,x,xthroat,Mdot,P0,T0,R)
        #Mach_Equation,gamma,nozzle_rad,x,xthroat,Mass_Flux,P_inlet,T_inlet,R
        

        plt.figure(1,figsize=(12, 6))
        plt.plot(x, nozzle_rad, 'k-', linewidth=2)  # Top boundary
        plt.plot(x, -nozzle_rad, 'k-', linewidth=2)  # Bottom boundary
        plt.xlabel("Axial Position (m)")
        plt.ylabel("Radial Position (m)")
        plt.title('Mach Number Plot')

        y = np.linspace(-Din,Din,200) #radial position vector for plotting

        X, Y = np.meshgrid(x, y) #meshgrid for mach num heat map

        upper_bound = nozzle_rad  # Upper boundary of the nozzle
        lower_bound = -nozzle_rad  # Lower boundary of the nozzle for 

        mask = (Y > upper_bound[np.newaxis, :]) | (Y < lower_bound[np.newaxis, :]) #mask for the plot, in order to exclude the values above and below the nozzle
        Mach_Plot = np.tile(mach_vec, (len(y), 1))  # Create a 2D Mach number array
        Mach_Plot[mask] = np.nan  # Set values outside the nozzle to NaN
        plt.contourf(X, Y, Mach_Plot, levels=50, cmap='jet')
        plt.colorbar(label="Mach Number")

        plt.grid()
        plt.show()

    def back_to_notescreen(self,instance):

        self.manager.current = 'third'
        ConfigManager(self).obtain_config_list()
        ConfigScreen().update_config_list(Folder_Path)

        #removes equation notescreen
        self.manager.remove_widget(self)


#App Class
class MERocketApp2(App):
    def build(self):

        screen_manager = ScreenManager(transition = NoTransition()) 

        home_screen = HomeScreen(name='home')
        input_screen = InputScreen(name='second')
        config_screen = ConfigScreen(name='third')

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(input_screen)
        screen_manager.add_widget(config_screen)
    
        return screen_manager


#Run Program
if __name__ == '__main__':
    MERocketApp2().run()