## GUI IMPORTS
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Separator, Notebook, Combobox
from tkinter.ttk import Button as TButton
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import messagebox
import ttkthemes
from ttkbootstrap import Style

# Ginga Imports
from ginga.tkw.ImageViewTk import ImageViewCanvas
from ginga.misc import log
from ginga.util.loader import load_data
from argparse import ArgumentParser
from ginga.AutoCuts import ZScale
from ginga.AutoCuts import Minmax
from ginga import GingaPlugin
from ginga.gw import Widgets
from ginga.gw import ColorBar

# Imexam
from imexam.imexamine import Imexamine
plots = Imexamine()
import imexam
# astropy
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# OS IMPORTS
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
import threading
import queue
from datetime import datetime
import sys
import glob
from os import path
from os import listdir
from os.path import isfile, join
import requests

# SELF IMPORTS
import Camera_Thread
import Calculated_Values


# constants
CORE_UPDATE_TICK = 1000
UI_FONT_SIZE = 9
os.environ['PATH'] = os.environ['PATH'] + ':/opt/local/bin'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Custom RadioButton  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class CustomRadiobutton(tk.Canvas):
    def __init__(self, master=None, width=None, height=None, callback=None, colors=None, status=None, text=None, **kwargs):
        super().__init__(master, borderwidth=0, highlightthickness=0, width=width, height=height, **kwargs)
        self.callback = callback
        self.bind("<Button-1>", self.on_click)
        self.status = status
        self.Colors = colors
        self.width = width-1
        self.height = height-1
        self.textpos_x = int(0.5*self.width)
        self.textpos_y = int(0.5*self.height)
        self.indpos_x_1 = int(0.1*self.textpos_x) 
        self.indpos_y_1 = int(0.5*self.textpos_y)
        self.radius_1 = self.height - 2*self.indpos_y_1
        self.indpos_x_2 = int((self.indpos_x_1 + 0.5*self.radius_1) - 0.125*self.radius_1)        
        self.indpos_y_2 = int((self.indpos_y_1 + 0.5*self.radius_1) - 0.125*self.radius_1)
        self.radius_2 = self.indpos_x_2 - self.indpos_x_1
        self.text = text
        if "on" in self.status:
            self.draw_custom_on()
        elif "off" in self.status:
            self.draw_custom_off()
        else:
            pass
        
    def draw_custom_off(self):
        darkest = self.Colors[4]   
        lightest = self.Colors[5]
        button_fill = self.Colors[1]
        text_fill = self.Colors[5]
        indicator_outline = self.Colors[5]
        indicator_fill = self.Colors[4]
        try:
            self.delete(self.on_oval_1)
            self.delete(self.on_oval_2)
            self.delete(self.on_rectangle)        
            self.delete(self.on_left_line_1)
            self.delete(self.on_left_line_2)
            self.delete(self.on_top_line_1)
            self.delete(self.on_top_line_2)
            self.delete(self.on_bot_line_1)
            self.delete(self.on_bot_line_2)
            self.delete(self.on_right_line_1)
            self.delete(self.on_right_line_2)
            self.delete(self.on_text)
        except:
            pass        
        # Rectangle (Darkest)
        self.off_rectangle = self.create_rectangle(0, 0, self.width, self.height, fill=button_fill, outline=darkest)
        # Oval 
        self.off_oval = self.create_oval(self.indpos_x_1, self.indpos_y_1, self.indpos_x_1 + self.radius_1, self.indpos_y_1 + self.radius_1,
                                                fill=indicator_fill, outline=indicator_outline)
        # Left Line
        self.off_left_line_1 = self.create_line(0,0,0,self.height-0, fill=lightest, width=1)
        self.off_left_line_2 = self.create_line(1,0,1,self.height-1, fill=lightest, width=1)
        # Top Line
        self.off_top_line_1 = self.create_line(0,0,self.width-0,0, fill=lightest, width=1)
        self.off_top_line_2 = self.create_line(0,1,self.width-1,1, fill=lightest, width=1)
        # Bottom Line
        self.off_bot_line_1 = self.create_line(0,self.height-0,self.width,self.height-0, fill=darkest, width=1)
        self.off_bot_line_2 = self.create_line(1,self.height-1,self.width,self.height-1, fill=darkest, width=1)
        # Right Line
        self.off_right_line_1 = self.create_line(self.width-0,0,self.width-0,self.height-1, fill=darkest, width=1)
        self.off_right_line_2 = self.create_line(self.width-1,1,self.width-1,self.height-2, fill=darkest, width=1)     
        # text
        self.off_text = self.create_text(self.textpos_x, self.textpos_y, text=self.text, fill=text_fill, font=('Courier', 18))

    def draw_custom_on(self):        
        # red = FF3864
        darkest = self.Colors[5]   
        lightest = self.Colors[6]
        button_fill = self.Colors[1]
        text_fill = self.Colors[7]
        indicator_outline = self.Colors[5]
        indicator_fill = self.Colors[4]
        indicator_mark_outline = self.Colors[6]
        indicator_mark_fill = self.Colors[8]
        try:
            self.delete(self.off_rectangle)        
            self.delete(self.off_left_line_1)
            self.delete(self.off_left_line_2)
            self.delete(self.off_top_line_1)
            self.delete(self.off_top_line_2)
            self.delete(self.off_bot_line_1)
            self.delete(self.off_bot_line_2)
            self.delete(self.off_right_line_1)
            self.delete(self.off_right_line_2)
            self.delete(self.off_text)
        except:
            pass
        # Rectangle (Darkest)
        self.on_rectangle = self.create_rectangle(0, 0, self.width, self.height, fill=button_fill, outline=darkest)
        # Oval 1
        self.on_oval_1 = self.create_oval(self.indpos_x_1, self.indpos_y_1, self.indpos_x_1 + self.radius_1, self.indpos_y_1 + self.radius_1,
                                                fill=indicator_fill, outline=indicator_outline)
        # Oval 2
        self.on_oval_2 = self.create_oval(self.indpos_x_2, self.indpos_y_2, self.indpos_x_2 + self.radius_2, self.indpos_y_2 + self.radius_2,
                                                fill=indicator_mark_fill, outline=indicator_mark_outline)
        # Left Line
        self.on_left_line_1 = self.create_line(0,0,0,self.height-0, fill=lightest, width=1)
        self.on_left_line_2 = self.create_line(1,0,1,self.height-1, fill=lightest, width=1)
        # Top Line
        self.on_top_line_1 = self.create_line(0,0,self.width-0,0, fill=lightest, width=1)
        self.on_top_line_2 = self.create_line(0,1,self.width-1,1, fill=lightest, width=1)
        # Bottom Line
        self.on_bot_line_1 = self.create_line(0,self.height-0,self.width,self.height-0, fill=darkest, width=1)
        self.on_bot_line_2 = self.create_line(1,self.height-1,self.width,self.height-1, fill=darkest, width=1)
        # Right Line
        self.on_right_line_1 = self.create_line(self.width-0,0,self.width-0,self.height-1, fill=darkest, width=1)
        self.on_right_line_2 = self.create_line(self.width-1,1,self.width-1,self.height-2, fill=darkest, width=1)     
        # text
        self.on_text = self.create_text(self.textpos_x, self.textpos_y, text=self.text, fill=text_fill, font=('Courier', 18))

    def on_click(self, event):              
        if self.callback:
            self.callback()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Custom CheckButton  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #          
class CustomCheckbutton(tk.Canvas):
    def __init__(self, master=None, width=None, height=None, callback=None, colors=None,  **kwargs):
        super().__init__(master, borderwidth=0, highlightthickness=0, width=width, height=height, **kwargs)
        self.callback = callback
        self.bind("<Button-1>", self.on_click)
        self.button_state = 0
        self.Colors = colors
        self.width = width-1
        self.height = height-1
        self.textpos_x = int(0.5*self.width)
        self.textpos_y = int(0.5*self.height)        
        self.draw_custom_off()        

    def draw_custom_off(self):
        darkest = self.Colors[1]
        second_darkest = self.Colors[2]
        lightest = self.Colors[6]
        # Make middle-of-the-road color
        HEX_1 = self.Colors[2].lstrip('#')
        HEX_2 = self.Colors[3].lstrip('#')
        RGB_1 = tuple(int(HEX_1[i:i+2], 16) for i in (0, 2, 4))
        RGB_2 = tuple(int(HEX_2[i:i+2], 16) for i in (0, 2, 4))
        RGB_av = (int(0.5*(RGB_1[0] + RGB_2[0])), int(0.5*(RGB_1[1] + RGB_2[1])), int(0.5*(RGB_1[2] + RGB_2[2])))
        Hex_Av = '#%02x%02x%02x' % RGB_av
        button_fill = Hex_Av
        text_fill = self.Colors[6]
        try:
            self.delete(self.on_rectangle)        
            self.delete(self.on_left_line_1)
            self.delete(self.on_left_line_2)
            self.delete(self.on_left_line_3)
            self.delete(self.on_top_line_1)
            self.delete(self.on_top_line_2)
            self.delete(self.on_top_line_3)
            self.delete(self.on_bot_line_1)
            self.delete(self.on_bot_line_2)
            self.delete(self.on_right_line_1)
            self.delete(self.on_right_line_2)
            self.delete(self.on_text)
        except:
            pass
        # Rectangle (Darkest)
        self.off_rectangle = self.create_rectangle(0, 0, self.width, self.height, fill=button_fill, outline=second_darkest)
        # Left Line
        self.off_left_line_1 = self.create_line(0,0,0,self.height-0, fill=lightest, width=1)
        self.off_left_line_2 = self.create_line(1,0,1,self.height-1, fill=lightest, width=1)
        # Top Line
        self.off_top_line_1 = self.create_line(0,0,self.width-0,0, fill=lightest, width=1)
        self.off_top_line_2 = self.create_line(0,1,self.width-1,1, fill=lightest, width=1)
        # Bottom Line
        self.off_bot_line_1 = self.create_line(0,self.height-1,self.width,self.height-1, fill=darkest, width=1)
        self.off_bot_line_2 = self.create_line(1,self.height-2,self.width,self.height-2, fill=darkest, width=1)
        # Right Line
        self.off_right_line_1 = self.create_line(self.width-0,0,self.width-0,self.height-1, fill=darkest, width=1)
        self.off_right_line_2 = self.create_line(self.width-1,1,self.width-1,self.height-2, fill=darkest, width=1)      
        self.off_text = self.create_text(self.textpos_x, self.textpos_y, text="Off", fill=text_fill, font=('Courier', 18))
        self.button_state = 0
        return self.button_state

    def draw_custom_on(self):
        # red = FF3864
        # Make middle-of-the-road color
        HEX_1 = self.Colors[2].lstrip('#')
        HEX_2 = self.Colors[3].lstrip('#')
        RGB_1 = tuple(int(HEX_1[i:i+2], 16) for i in (0, 2, 4))
        RGB_2 = tuple(int(HEX_2[i:i+2], 16) for i in (0, 2, 4))
        RGB_av = (int(0.5*(RGB_1[0] + RGB_2[0])), int(0.5*(RGB_1[1] + RGB_2[1])), int(0.5*(RGB_1[2] + RGB_2[2])))
        Hex_Av = '#%02x%02x%02x' % RGB_av
        darkest = self.Colors[1]
        second_darkest = self.Colors[2]
        lightest = self.Colors[7]
        second_lightest = self.Colors[6]
        button_fill = Hex_Av
        text_fill = self.Colors[7]
        try:
            self.delete(self.off_rectangle)        
            self.delete(self.off_left_line_1)
            self.delete(self.off_left_line_2)
            self.delete(self.off_top_line_1)
            self.delete(self.off_top_line_2)
            self.delete(self.off_bot_line_1)
            self.delete(self.off_bot_line_2)
            self.delete(self.off_right_line_1)
            self.delete(self.off_right_line_2)
            self.delete(self.off_text)
        except:
            pass
        # Rectangle (Darkest)
        self.on_rectangle = self.create_rectangle(0, 0, self.width, self.height, fill=button_fill, outline=darkest)
        # Left Line
        self.on_left_line_1 = self.create_line(0,0,0,self.height-0, fill=darkest, width=1)
        self.on_left_line_2 = self.create_line(1,0,1,self.height-1, fill=second_darkest, width=1)
        self.on_left_line_3 = self.create_line(2,0,2,self.height-2, fill=second_darkest, width=1)
        # Top Line
        self.on_top_line_1 = self.create_line(0,0,self.width-0,0, fill=darkest, width=1)
        self.on_top_line_2 = self.create_line(0,1,self.width-1,1, fill=second_darkest, width=1)
        self.on_top_line_3 = self.create_line(0,2,self.width-2,2, fill=second_darkest, width=1)
        # Bottom Line
        self.on_bot_line_1 = self.create_line(0,self.height-1,self.width,self.height-1, fill=lightest, width=1)
        self.on_bot_line_2 = self.create_line(1,self.height-2,self.width,self.height-2, fill=second_lightest, width=1)
        # Right Line
        self.on_right_line_1 = self.create_line(self.width-0,0,self.width-0,self.height-1, fill=lightest, width=1)
        self.on_right_line_2 = self.create_line(self.width-1,1,self.width-1,self.height-2, fill=second_lightest, width=1)     
        # text
        self.on_text = self.create_text(self.textpos_x, self.textpos_y, text="On", fill=text_fill, font=('Courier', 18))
        self.button_state = 1
        return self.button_state

    def on_click(self, event):
        if self.button_state == 0:
            self.draw_custom_on()
        else:
            self.draw_custom_off()
        if self.callback:
            self.callback()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
class Camera_Options(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Camera Options")
        self.master.geometry("1950x1010+10+1")
        self.master.topmost= True
        self.master.takefocus=True
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.focus_set()
        self.running = False
        self.Camera_Queue_In = queue.Queue()
        self.Camera_Queue_Out = queue.Queue()
        self.Command_Queue = queue.Queue()
        # Frame Vars
        self.apply_to_all = IntVar()
        # Tab Vars
        self.main_sensor_state_1 = 0
        self.main_sensor_state_2 = 0
        self.camera_2_name = "Bobwhite"
        self.camera_1_name = "Harlequin"
         # Exposure Times
        self.exposure_time_1 = 0.12
        self.exposure_time_2 = 0.12
        # Serials
        self.serial_number_1 = "AL3200M-18070201"
        self.serial_number_2 = "AL3200M-18070401"
         # Filter Setting
        self.filter_1 = 0
        self.filter_2 = 0
        # Setpoints
        self.setpoint_1 = 0
        self.setpoint_2 = 0
        # Shutters
        self.shutter_1 = 0
        self.shutter_2 = 0
        # Frame Types
        self.frametype_1 = 0
        self.frametype_2 = 0
        # Binning
        self.binning_1 = 0
        self.binning_2 = 0
        # Readouts
        self.readout_1 = 0
        self.readout_2 = 0
        # overscan
        self.overscan_1 = 0
        self.overscan_2 = 0
        # overscan
        self.window_heater_1 = 0
        self.window_heater_2 = 0
        # X Bin
        self.xbin_1 = 1
        self.xbin_2 = 1
        # Y Bin
        self.ybin_1 = 1
        self.ybin_2 = 1
        # Object Name
        self.object_name = "Image_Camera_1"
        # Epoch 1
        self.epoch = StringVar()
        self.RA_H = StringVar()
        self.RA_M = StringVar()
        self.RA_S = StringVar()
        self.DEC_D = StringVar()
        self.DEC_M = StringVar()
        self.DEC_S = StringVar()       
        # User Exposure Time Settings
        self.user_exposure_time_1 = StringVar()
        self.user_exposure_time_2 = StringVar()
        # User Series Settings
        self.user_series_1 = StringVar()
        self.user_series_2 = StringVar()
        # User Filter Setting
        self.user_filter_1 = StringVar()
        self.user_filter_2 = StringVar()
        # User Shutter Mode Settings
        self.user_shutter_1 = StringVar()
        self.user_shutter_2 = StringVar()
        # User Binning Settings
        self.user_binning_1 = StringVar()
        self.user_binning_2 = StringVar()        
        # User Readout Mode Settings
        self.user_readout_1 = StringVar()
        self.user_readout_2 = StringVar()
        # User CCD Setpoint Settings
        self.user_set_point_1 = StringVar()
        self.user_set_point_2 = StringVar()
        # User Status Led Settings
        self.user_status_led_1 = IntVar()
        self.user_status_led_2 = IntVar()
        # User Window Heater Settings
        self.user_window_heater_1 = IntVar()
        self.user_window_heater_2 = IntVar()
        # User Overscan Settings
        self.user_overscan_1 = IntVar()
        self.user_overscan_2 = IntVar()
        # User Preflash Duration Setting
        self.user_preflash_duration_1 = StringVar()
        self.user_preflash_duration_2 = StringVar()
        # User Preflash Clearouts Settings
        self.user_preflash_clearout_1 = StringVar()
        self.user_preflash_clearout_2 = StringVar()
        # User Object Name
        self.user_object_name = StringVar()     
        # Cooling Status as reported by camera
        self.cooling_enabled_1 = 0
        self.cooling_enabled_2 = 0
        # birger setpoints
        self.birger_setpoint_1 = 0
        self.max_birger_setpoint_1 = 0
        self.birger_scale_setpoint_1 = IntVar()
        self.birger_entry_setpoint_1 = StringVar()
        self.birger_setpoint_2 = 0
        self.max_birger_setpoint_2 = 0
        self.birger_scale_setpoint_2 = IntVar()
        self.birger_entry_setpoint_2 = StringVar()      
        # Is there an exposure going
        self.ongoing_exposure_1 = 0
        self.ongoing_exposure_2 = 0
        # We can only issue the readout command once
        self.readout_issued = []
        self.timer_counter_1 = 0
        self.fig_1 = None
        self.fig_2 = None
        # Ginga Viewer Stuff
        argprs = ArgumentParser()
        argprs.add_argument("--debug", dest="debug", default=False,
                        action="store_true",
                        help="Enter the pdb debugger on main()")
        argprs.add_argument("--profile", dest="profile", action="store_true",
                        default=False,
                        help="Run the profiler on main()")
        log.addlogopts(argprs)
        (options, args) = argprs.parse_known_args(sys.argv[1:])
        self.logger = log.get_logger("example2", options=options)
        # Gui Counters Stuff
        # Camera 1
        sv1 = np.arange(0, 101, 1)
        self.pressed_zoom_count_1 = 0
        self.pressed_scale_count_1 = 0
        self.pressed_aperphot_count_1 = 0
        self.pressed_zoom_in_1 = 0
        self.pressed_zoom_out_1 = 0
        self.zoom_fit_value_1 = None
        self.current_zoom_value_1 = None
        self.scale_contrast_value_1 = DoubleVar()
        self.scale_1 = "minmax"
        self.scale_type_1 = None
        self.meanval = 0.5        
        self.scale_vector_val = sv1/100
        self.tag_count_1 = 0
        self.canvas_tag_1 = None
        self.timer_counter_2 = 0
        # Camera 2
        self.pressed_zoom_count_2 = 0
        self.pressed_scale_count_2 = 0
        self.pressed_aperphot_count_2 = 0
        self.pressed_zoom_in_2 = 0
        self.pressed_zoom_out_2 = 0
        self.zoom_fit_value_2 = None
        self.current_zoom_value_2 = None
        self.scale_contrast_value_2 = DoubleVar()
        self.scale_2 = "minmax"
        self.scale_type_2 = None
        self.meanval = 0.5        
        self.scale_vector_val_2 = sv1/100
        # Readout Command
        self.readout_command_issued_1 = 0
        self.readout_command_issued_2 = 0
        # Autofocusing
        self.xcentroids_1 = []
        self.ycentroids_1 = []
        self.xcentroids_2 = []
        self.ycentroids_2 = []
        self.pressed_autofocus_count_1 = 0
        self.pressed_autofocus_count_2 = 0
        self.pressed_autofocus_count_3 = 0
        self.pressed_autofocus_count_4 = 0
        self.Autofocus_Queue_In_1 = queue.Queue()
        self.Autofocus_Queue_Out_1 = queue.Queue()
        self.Autofocus_Queue_In_2 = queue.Queue()
        self.Autofocus_Queue_Out_2 = queue.Queue()
        self.autofocusing_setpoint_1_1 = 21500
        self.autofocusing_setpoint_1_2 = 21400
        self.autofocusing_setpoint_1_3 = 21600
        self.autofocusing_iteration_2 = 0
        self.fwhm_array_1 = []
        self.fwhm_array_2 = []
        self.r_1 = 10
        self.r_2 = 10
        self.fwhm_radii_1 = []
        self.autofocus_image_array_1 = []
        self.FWHM_array_1 = []
        self.autofocusing_iteration_1 = 0
        # Start the program
        self.initUI()
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Draw GUI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
    def initUI(self):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #      
        self.Main_Frame = ttk.Frame(self.master, width=2000, height=1010)
        self.Main_Frame.grid(row=0, column=0, sticky=N)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Colors ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.Harlequin_Colors = ["#190714", "#2D0829", "#410A3E", "#553252", "#9A5885", "#C87AAD", "#E198B5", "#F4B8C0", "#F8DCD9"]
        self.Bobwhite_Colors = ["#05140A", "#0B2D3D", "#0B4151", "#025F67", "#017E78", "#329D85", "#66BB8C", "#9BD894", "#D4F3A3"]      
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.style = ttkthemes.ThemedStyle()
        self.style.theme_use('black')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
        # Harlequin
        self.style.configure("Harlequin.TFrame", background=self.Harlequin_Colors[0], relief="flat")
        # Top Frame (Camera Settings, Focus Settings, Object Settings)
        self.style.configure('Harlequin.TLabelframe.Label',font=("Courier", "22"), foreground=self.Harlequin_Colors[7], background=self.Harlequin_Colors[0])
        self.style.configure('Harlequin.TLabelframe', relief="ridge", background=self.Harlequin_Colors[0], borderwidth=3, bordercolor=self.Harlequin_Colors[5],
                             lightcolor=self.Harlequin_Colors[5], darkcolor=self.Harlequin_Colors[5])
        # Label (Exposure Settings, Temperature Settings)
        self.style.configure('HarlequinThird.TLabel',font=("Courier", "20"), foreground=self.Harlequin_Colors[7], background=self.Harlequin_Colors[0])
        # Separator
        self.style.configure("Harlequin.TSeparator", background=self.Harlequin_Colors[6])
        # Labels for Interactibles
        self.style.configure('HarlequinFourth.TLabel', font=("Courier", "18"), foreground=self.Harlequin_Colors[6], background=self.Harlequin_Colors[0])
        # Disabled Entry-Looking Label
        self.style.configure('HarlequinFake.TLabel', font=("Courier", "18"), relief="ridge", justify='center', foreground=self.Harlequin_Colors[7],
                             background=self.Harlequin_Colors[1], borderwidth=3, bordercolor = self.Harlequin_Colors[5],
                             lightcolor=self.Harlequin_Colors[6], darkcolor=self.Harlequin_Colors[4])
        # Entries in Settings
        self.style.configure('Harlequin.TEntry', foreground=self.Harlequin_Colors[8],background=self.Harlequin_Colors[0], relief="ridge",
                             fieldbackground=self.Harlequin_Colors[1], selectbackground=self.Harlequin_Colors[2],
                             insertwidth=1, insertcolor=self.Harlequin_Colors[8], bordercolor=self.Harlequin_Colors[5],
                             selectforeground=self.Harlequin_Colors[8],
                             lightcolor=self.Harlequin_Colors[6], darkcolor=self.Harlequin_Colors[4])
        # Right Hand Side Image Values        
        self.style.configure('HarlequinSmall.TLabel', font=("Courier", "18"), foreground=self.Harlequin_Colors[8], background=self.Harlequin_Colors[0])
        # ComboBox        
        self.style.configure("Harlequin.TCombobox", font=("Courier", "18"), justify="center", foreground=self.Harlequin_Colors[8], background=self.Harlequin_Colors[0],
                             fieldbackground=self.Harlequin_Colors[1], selectbackground=self.Harlequin_Colors[2],
                             selectforeground=self.Harlequin_Colors[7], bordercolor=self.Harlequin_Colors[5],
                             lightcolor=self.Harlequin_Colors[6], darkcolor=self.Harlequin_Colors[4], arrowcolor=self.Harlequin_Colors[5])
        # Buttons
        self.style.configure("HarlequinRaisedButton.TButton",relief="raised", font=("Courier", "20"),
                             borderwidth=1, bordercolor = self.Harlequin_Colors[6], lightcolor=self.Harlequin_Colors[8], darkcolor=self.Harlequin_Colors[4],
                             foreground=self.Harlequin_Colors[7], background=self.Harlequin_Colors[2],  anchor="center")
        self.style.map("HarlequinRaisedButton.TButton",
                       relief=[("pressed", "sunken"), ("active", "raised")],
                       foreground=[("pressed", self.Harlequin_Colors[7]), ("active", self.Harlequin_Colors[8])],
                       background=[("pressed", "!disabled", self.Harlequin_Colors[2]), ("active", self.Harlequin_Colors[2])],
                       bordercolor=[("pressed", "!disabled", self.Harlequin_Colors[6]), ("active", self.Harlequin_Colors[7])])        
        self.style.configure("HarlequinSunkenButton.TButton",relief="sunken", font=("Courier", "20"),
                             borderwidth=1, bordercolor = self.Harlequin_Colors[6], lightcolor=self.Harlequin_Colors[8], darkcolor=self.Harlequin_Colors[4],
                             foreground=self.Harlequin_Colors[6], background=self.Harlequin_Colors[1],  anchor="center")
        self.style.map("HarlequinSunkenButton.TButton",
                       relief=[('active','sunken'),('pressed', 'raised')],
                       background=[('active',self.Harlequin_Colors[0])])    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #  
        # Bobwhite
        self.style.configure("Bobwhite.TFrame", background=self.Bobwhite_Colors[0], relief="flat", borderwidth=0)
        # Top Frame (Camera Settings, Focus Settings, Object Settings)
        self.style.configure('Bobwhite.TLabelframe.Label',font=("Courier", "22"), foreground=self.Bobwhite_Colors[7], background=self.Bobwhite_Colors[0])
        self.style.configure('Bobwhite.TLabelframe', relief="ridge", background=self.Bobwhite_Colors[0], borderwidth=3, bordercolor=self.Bobwhite_Colors[5],
                             lightcolor=self.Bobwhite_Colors[5], darkcolor=self.Bobwhite_Colors[5])
        # Label (Exposure Settings, Temperature Settings)
        self.style.configure('BobwhiteThird.TLabel',font=("Courier", "20"), foreground=self.Bobwhite_Colors[7], background=self.Bobwhite_Colors[0])
        # Separator
        self.style.configure("Bobwhite.TSeparator", background=self.Bobwhite_Colors[6])
        # Labels for Interactibles
        self.style.configure('BobwhiteFourth.TLabel', font=("Courier", "18"), foreground=self.Bobwhite_Colors[6], background=self.Bobwhite_Colors[0])
        # Disabled Entry-Looking Label
        self.style.configure('BobwhiteFake.TLabel', font=("Courier", "18"), relief="ridge", justify='center', foreground=self.Bobwhite_Colors[7],
                             background=self.Bobwhite_Colors[1], borderwidth=3, bordercolor = self.Bobwhite_Colors[5],
                             lightcolor=self.Bobwhite_Colors[6], darkcolor=self.Bobwhite_Colors[4])
        # Entries in Settings
        self.style.configure('Bobwhite.TEntry', foreground=self.Bobwhite_Colors[8],background=self.Bobwhite_Colors[0], relief="ridge",
                             fieldbackground=self.Bobwhite_Colors[1], selectbackground=self.Bobwhite_Colors[2],
                             insertwidth=1, insertcolor=self.Bobwhite_Colors[8], bordercolor=self.Bobwhite_Colors[5],
                             selectforeground=self.Bobwhite_Colors[8],
                             lightcolor=self.Bobwhite_Colors[6], darkcolor=self.Bobwhite_Colors[4])
        # ComboBox        
        self.style.configure("Bobwhite.TCombobox", font=("Courier", "18"), justify="center", foreground=self.Bobwhite_Colors[8], background=self.Bobwhite_Colors[0],
                             fieldbackground=self.Bobwhite_Colors[1], selectbackground=self.Bobwhite_Colors[2],
                             selectforeground=self.Bobwhite_Colors[7], bordercolor=self.Bobwhite_Colors[5],
                             lightcolor=self.Bobwhite_Colors[6], darkcolor=self.Bobwhite_Colors[4], arrowcolor=self.Bobwhite_Colors[5])
        # Buttons
        self.style.configure("BobwhiteRaisedButton.TButton",relief="raised", font=("Courier", "20"), 
                        borderwidth=3, foreground=self.Bobwhite_Colors[7], lightcolor=self.Bobwhite_Colors[6], darkcolor=self.Bobwhite_Colors[4],
                        background=self.Bobwhite_Colors[1], bordercolor = self.Bobwhite_Colors[5], anchor="center")        
        self.style.map("BobwhiteRaisedButton.TButton",
                       relief=[("pressed", "sunken"), ("active", "raised")],
                       foreground=[("pressed", self.Bobwhite_Colors[7]), ("active", self.Bobwhite_Colors[8])],
                       background=[("pressed", "!disabled", self.Bobwhite_Colors[2]), ("active", self.Bobwhite_Colors[2])],
                       bordercolor=[("pressed", "!disabled", self.Bobwhite_Colors[6]), ("active", self.Bobwhite_Colors[7])])
        self.style.configure("BobwhiteSunkenButton.TButton",relief="sunken", font=("Courier", "20"), 
                        borderwidth=3, lightcolor=self.Bobwhite_Colors[6], darkcolor=self.Bobwhite_Colors[4],
                        foreground=self.Bobwhite_Colors[2], background=self.Bobwhite_Colors[0], bordercolor = self.Bobwhite_Colors[1], anchor="center")
        self.style.map("BobwhiteSunkenButton.TButton",
                       relief=[('active','sunken'),('pressed', 'raised')],
                       background=[('active',self.Bobwhite_Colors[0])])
        # Right Hand Side Image Values        
        self.style.configure('BobwhiteSmall.TLabel', font=("Courier", "18"), foreground=self.Bobwhite_Colors[8], background=self.Bobwhite_Colors[0])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Common Style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #  
        # Common
        self.Common_Colors = ["#070030", "#120854", "#26195F", "#005D9E", '#0095AF','#19BDB0', '#9ADCBB','#D7F4CF','#FCFFDD' ]
        # Top Frame (Camera Settings, Focus Settings, Object Settings)
        self.style.configure('Common.TLabelframe.Label',font=("Courier", "22"), foreground=self.Common_Colors[6], background=self.Common_Colors[0])
        self.style.configure('Common.TLabelframe', relief="ridge", background=self.Common_Colors[0], borderwidth=3, bordercolor=self.Common_Colors[5],
                             lightcolor=self.Common_Colors[5], darkcolor=self.Common_Colors[5])
        # Labels for Interactibles
        self.style.configure('CommonFourth.TLabel', font=("Courier", "18"), foreground=self.Common_Colors[6], background=self.Common_Colors[0])
        # Disabled Entry-Looking Label
        self.style.configure('CommonFake.TLabel', font=("Courier", "18"), relief="ridge", justify='center', foreground=self.Common_Colors[7],
                             background=self.Common_Colors[1], borderwidth=3, bordercolor = self.Common_Colors[5],
                             lightcolor=self.Common_Colors[6], darkcolor=self.Common_Colors[4])
        # Entries in Object
        self.style.configure('Common.TEntry', foreground=self.Common_Colors[8],background=self.Common_Colors[0], relief="ridge",
                             fieldbackground=self.Common_Colors[1], selectbackground=self.Common_Colors[2],
                             insertwidth=1, insertcolor=self.Common_Colors[8], bordercolor=self.Common_Colors[5],
                             selectforeground=self.Common_Colors[8],
                             lightcolor=self.Common_Colors[6], darkcolor=self.Common_Colors[4])        
        # Buttons
        self.style.configure("CommonRaisedButton.TButton",relief="raised", font=("Courier", "20"), 
                        borderwidth=3, foreground=self.Common_Colors[6], lightcolor=self.Common_Colors[6], darkcolor=self.Common_Colors[4],
                        background=self.Common_Colors[1], bordercolor = self.Common_Colors[4], anchor="center")
        self.style.map("CommonRaisedButton.TButton",
                       relief=[("pressed", "sunken"), ("active", "raised")],
                       foreground=[("pressed", self.Common_Colors[8]), ("active", self.Common_Colors[7])],
                       background=[("pressed", "!disabled", self.Common_Colors[1]), ("active", self.Common_Colors[2])],
                       bordercolor=[("pressed", "!disabled", self.Common_Colors[5]), ("active", self.Common_Colors[6])])
        self.style.configure("CommonSunkenButton.TButton",relief="sunken", font=("Courier", "20"), 
                        borderwidth=3, lightcolor=self.Common_Colors[6], darkcolor=self.Common_Colors[4],
                        foreground=self.Common_Colors[2], background=self.Common_Colors[0], bordercolor = self.Common_Colors[1], anchor="center")

        self.style.configure('Error.TEntry', foreground="red" ,background="#200000", relief="ridge",
                             fieldbackground="#200000", selectbackground="#400000",
                             insertwidth=1, insertcolor="#400000", bordercolor="#800000",
                             selectforeground="#800000",
                             lightcolor="#800000", darkcolor="#100000")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Overall Style Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #        
        self.master.option_add('*TEntry.font', ('Courier', 18))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tab and Notebook ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #          
        # Parent Tab
        self.tab_parent = ttk.Notebook(self.Main_Frame, style="TNotebook")
        # Tab Camera 1
        self.tab_1 = ttk.Frame(self.tab_parent, style="Harlequin.TFrame")              
        # Tab Camera 2
        self.tab_2 = ttk.Frame(self.tab_parent, style="Bobwhite.TFrame")
        # Add tabs to the notebook
        self.tab_parent.add(self.tab_1, text=" Harlequin ") 
        self.tab_parent.add(self.tab_2, text=" Bobwhite ")
        # Place Tabs
        self.tab_parent.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.tab_parent.grid(row=0, column=0, sticky=N, padx=(5,5), pady = (0,0))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Common Buttons Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
        self.All_Cameras_Button_Frame = ttk.LabelFrame(self.Main_Frame, text="Control Both CCDs", style='Common.TLabelframe', width=860, height=110, labelanchor='n')
        self.All_Cameras_Button_Frame.columnconfigure(index=0, weight=1, minsize=210)
        self.All_Cameras_Button_Frame.columnconfigure(index=1, weight=1, minsize=210)
        self.All_Cameras_Button_Frame.columnconfigure(index=2, weight=1, minsize=210)
        self.All_Cameras_Button_Frame.columnconfigure(index=3, weight=1, minsize=210)
        self.All_Cameras_Button_Frame.grid(row=2, column=0, padx=(0,0), pady=(0,0), sticky=N)
        self.All_Cameras_Button_Frame.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Common Buttons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
        self.Cool_Button = ttk.Button(self.All_Cameras_Button_Frame, text=" Cool All ",  style="CommonRaisedButton.TButton",  command = self._cool_all)
        self.Cool_Button.grid(row=0, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Stop Cool Both
        self.Stop_Cooling = ttk.Button(self.All_Cameras_Button_Frame, text=" Stop Cooling All ",style="CommonRaisedButton.TButton",  command = self._stop_cooling_all)
        self.Stop_Cooling.grid(row=0, column=1, columnspan=1, padx=(2,5), pady=(3,3), sticky=E+W)
        # Expose Both
        self.Exposure_Button = ttk.Button(self.All_Cameras_Button_Frame, text=" Expose All ",  style="CommonRaisedButton.TButton", command = self._expose_all)
        self.Exposure_Button.grid(row=0, column=2, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Connect Camera 1
        self.Save_Folder_1 = ttk.Button(self.All_Cameras_Button_Frame, text=" Abort All ",   style="CommonRaisedButton.TButton",   command = self._abort_all)
        self.Save_Folder_1.grid(row=0, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Close Camera 1
        self.Close_Button_1 = ttk.Button(self.All_Cameras_Button_Frame, text=" Close ",  style="CommonRaisedButton.TButton", command = self._on_close)
        self.Close_Button_1.grid(row=1, column=3, columnspan=1, padx=(5,5), pady=(5,3), sticky=E+W)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Epoch Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
        # Buttons Frame Camera 1
        self.Object_Frame = ttk.LabelFrame(self.Main_Frame, text="Object Settings", style='Common.TLabelframe',width=860, height=255,labelanchor='n')
        self.Object_Frame.columnconfigure(index=0, weight=1, minsize=190)
        self.Object_Frame.columnconfigure(index=1, weight=1, minsize=220)
        self.Object_Frame.columnconfigure(index=2, weight=1, minsize=220)
        self.Object_Frame.columnconfigure(index=3, weight=1, minsize=220)
        self.Object_Frame.grid(row=1, column=0, columnspan=1, padx=(0,0), pady=(0,0), sticky=N)
        self.Object_Frame.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Epoch Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ # 
        ri = 0        
        # Object Name
        self.lbl_Object_Name = ttk.Label(self.Object_Frame, text="Object Name:", anchor='e',style="CommonFourth.TLabel")
        self.lbl_Object_Name.grid(row=ri, column=0, padx=(5,0), pady=(3,3), sticky=E+W)
        self.Object_Name_Entry = ttk.Entry(self.Object_Frame,style="Common.TEntry",justify='center',textvariable=self.user_object_name)
        self.Object_Name_Entry.grid(row=ri, column=1, columnspan=3, padx=(5,5), pady=(3,3), sticky=E+W)                                                         
        ri = ri+1
        # RA H
        self.lbl_RA_H = ttk.Label(self.Object_Frame, text="Hours", justify='center', anchor='s', style="CommonFourth.TLabel")
        self.lbl_RA_H.grid(row=ri, column=1, padx=(5,5),  pady=(5,0), sticky=E+W)
        # RA M
        self.lbl_RA_M = ttk.Label(self.Object_Frame, text="Minutes", justify='center', anchor='s', style="CommonFourth.TLabel")
        self.lbl_RA_M.grid(row=ri, column=2, padx=(5,5), pady=(5,0), sticky=E+W)
        # RA S
        self.lbl_RA_S = ttk.Label(self.Object_Frame, text="Seconds", justify='center', anchor='s',style="CommonFourth.TLabel")
        self.lbl_RA_S.grid(row=ri, column=3, padx=(5,5), pady=(5,0), sticky=E+W)
        ri = ri+1
        # RA Label
        self.lbl_RA = ttk.Label(self.Object_Frame, text="Right Ascension:", anchor='e',style="CommonFourth.TLabel")
        self.lbl_RA.grid(row=ri, column=0,columnspan=1, rowspan=1, padx=(5,0), pady=(0,0), sticky=E+W)        
        self.Entry_RA_H = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry",textvariable=self.RA_H)
        self.Entry_RA_H.grid(row=ri, column=1,  padx=(5,5), pady=(0,0), sticky=E+W)        
        self.Entry_RA_M = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry",textvariable=self.RA_M)
        self.Entry_RA_M.grid(row=ri, column=2,  padx=(5,5), pady=(0,0), sticky=E+W)        
        self.Entry_RA_S = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry",textvariable=self.RA_S)
        self.Entry_RA_S.grid(row=ri, column=3,  padx=(5,5), pady=(0,0), sticky=E+W)        
        ri=ri+1
        # DEC D
        self.lbl_DEC_D = ttk.Label(self.Object_Frame, text="Degrees", justify='center', anchor='s',style="CommonFourth.TLabel")
        self.lbl_DEC_D.grid(row=ri, column=1, padx=(5,5),  pady=(5,0), sticky=E+W)
        # RA M
        self.lbl_DEC_M = ttk.Label(self.Object_Frame, text="Minutes", justify='center', anchor='s',style="CommonFourth.TLabel")
        self.lbl_DEC_M.grid(row=ri, column=2, padx=(5,5), pady=(5,0), sticky=E+W)
        # RA S
        self.lbl_DEC_S = ttk.Label(self.Object_Frame, text="Seconds", justify='center', anchor='s',style="CommonFourth.TLabel")
        self.lbl_DEC_S.grid(row=ri, column=3, padx=(5,5), pady=(5,0), sticky=E+W)
        ri=ri+1
        # DEC Label
        self.lbl_DEC = ttk.Label(self.Object_Frame, text="Declination:", anchor="e", style="CommonFourth.TLabel")
        self.lbl_DEC.grid(row=ri, column=0,columnspan=1, rowspan=1, padx=(5,0), pady=(0,0), sticky=E+W)
        self.Entry_DEC_D = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry",textvariable=self.DEC_D)
        self.Entry_DEC_D.grid(row=ri, column=1,  padx=(5,5), pady=(0,0), sticky=E+W)        
        self.Entry_DEC_M = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry", textvariable=self.DEC_M)
        self.Entry_DEC_M.grid(row=ri, column=2,  padx=(5,5), pady=(0,0), sticky=E+W)        
        self.Entry_DEC_S = ttk.Entry(self.Object_Frame, justify='center', style="Common.TEntry",textvariable=self.DEC_S)
        self.Entry_DEC_S.grid(row=ri, column=3,  padx=(5,5), pady=(0,0), sticky=E+W)
        ri = ri+1        
        # Epoch
        self.lbl_Epoch = ttk.Label(self.Object_Frame, text="Epoch:", anchor='e',style="CommonFourth.TLabel")
        self.lbl_Epoch.grid(row=ri, column=0, padx=(5,0), pady=(10,5), sticky=E+W)        
        self.Epoch_2000 = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_2000,
                                                            colors=self.Common_Colors, status = "on", text="J2000")
        self.Epoch_2000.grid(row=5, column=1, padx=(5,5), pady=(10,5), sticky=E+W)        
        self.Epoch_Today = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_Today,
                                                        colors=self.Common_Colors, status = "off", text="Today")
        self.Epoch_Today.grid(row=5, column=2, padx=(5,5), pady=(10,5), sticky=E+W)
        # Precess
        self.Precess_Button = ttk.Button(self.Object_Frame, style = "CommonRaisedButton.TButton", text="Precess", command = self.precess)
        self.Precess_Button.grid(row=ri, column=3, columnspan=1, padx=(5,5), pady=(10,5), sticky=E+W)        
        ri=ri+1
        # Display Precessed RA Coordinates
        self.lbl_Precessed_RA = ttk.Label(self.Object_Frame, text="Precessed RA:",anchor="e",style="CommonFourth.TLabel")
        self.lbl_Precessed_RA.grid(row=ri, column=0, padx=(5,5), pady=(5,5), sticky=E+W)
        # RA 
        self.Precessed_RA = ttk.Label(self.Object_Frame, text="--", justify='center', relief="sunken", anchor='n', style="CommonFake.TLabel")
        self.Precessed_RA.grid(row=ri, column=1, padx=(5,5),  pady=(5,5), sticky=E+W)        
        # Display Precessed DEC Coordinates
        self.lbl_Precessed_DEC = ttk.Label(self.Object_Frame, text="Precessed DEC:", anchor="e",style="CommonFourth.TLabel")
        self.lbl_Precessed_DEC.grid(row=ri, column=2, padx=(5,5), pady=(5,5), sticky=E+W)
        # DEC
        self.Precessed_DEC = ttk.Label(self.Object_Frame, text="--", justify='center',relief="sunken", anchor='n', style="CommonFake.TLabel")
        self.Precessed_DEC.grid(row=ri, column=3, padx=(5,5),  pady=(5,5), sticky=E+W)   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #       
        # Camera Controls Frame Camera 1
        self.Camera_Controls_Frame_1 = ttk.LabelFrame(self.tab_1, text="Camera Settings", style='Harlequin.TLabelframe', width=850, height=440, labelanchor='n')
        column_minsize = 140
        self.Camera_Controls_Frame_1.columnconfigure(index=0, weight=1, minsize=200)
        self.Camera_Controls_Frame_1.columnconfigure(index=1, weight=1, minsize=200)
        self.Camera_Controls_Frame_1.columnconfigure(index=2, weight=1, minsize=200)
        self.Camera_Controls_Frame_1.columnconfigure(index=3, weight=1, minsize=200)
        self.Camera_Controls_Frame_1.rowconfigure(index=0, weight=0, minsize=25)  # exposure settings
        self.Camera_Controls_Frame_1.rowconfigure(index=1, weight=0, minsize=5)  # separator
        self.Camera_Controls_Frame_1.rowconfigure(index=2, weight=0, minsize=25)  # exposure, readout
        self.Camera_Controls_Frame_1.rowconfigure(index=3, weight=0, minsize=25)  # series, overscan
        self.Camera_Controls_Frame_1.rowconfigure(index=4, weight=0, minsize=25)  # filter, WH
        self.Camera_Controls_Frame_1.rowconfigure(index=5, weight=0, minsize=25)  # frame, preflash
        self.Camera_Controls_Frame_1.rowconfigure(index=6, weight=0, minsize=25)  # binning, flushes
        self.Camera_Controls_Frame_1.rowconfigure(index=7, weight=0, minsize=25)  # temperature settings
        self.Camera_Controls_Frame_1.rowconfigure(index=8, weight=0, minsize=5)  # separator
        self.Camera_Controls_Frame_1.rowconfigure(index=9, weight=0, minsize=25)  # ccd setpoint, ccd temperature
        self.Camera_Controls_Frame_1.rowconfigure(index=10, weight=0, minsize=25) # recommended temp, heat sink
        self.Camera_Controls_Frame_1.rowconfigure(index=12, weight=0, minsize=5) # cooling control, cooler power
        self.Camera_Controls_Frame_1.rowconfigure(index=13, weight=0, minsize=40) # separator
        self.Camera_Controls_Frame_1.grid(row=0, column=0, padx=(0,0), pady=(0,0), sticky=N)
        self.Camera_Controls_Frame_1.grid_propagate(0)
        # Birger Frame Camera 1
        self.Birger_Frame_1 = ttk.LabelFrame(self.tab_1, text="Focus Settings", style='Harlequin.TLabelframe', width=850, height= 110, labelanchor='n')
        self.Birger_Frame_1.columnconfigure(index=0, weight=1, minsize=200)
        self.Birger_Frame_1.columnconfigure(index=1, weight=1, minsize=225)
        self.Birger_Frame_1.columnconfigure(index=2, weight=1, minsize=200)
        self.Birger_Frame_1.columnconfigure(index=3, weight=2, minsize=185)
        self.Birger_Frame_1.grid(row=1, column=0,  padx=(5,5), pady=(5,5), sticky=N)
        self.Birger_Frame_1.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #      
        # Camera Controls Frame Camera 2
        self.Camera_Controls_Frame_2 = ttk.LabelFrame(self.tab_2, text="Camera Settings", style='Bobwhite.TLabelframe', width=850, height= 450, labelanchor='n')
        # Columns are horizontal
        self.Camera_Controls_Frame_2.columnconfigure(index=0, weight=1, minsize=210)
        self.Camera_Controls_Frame_2.columnconfigure(index=1, weight=1, minsize=210)
        self.Camera_Controls_Frame_2.columnconfigure(index=2, weight=1, minsize=210)
        self.Camera_Controls_Frame_2.columnconfigure(index=3, weight=1, minsize=210)
        # rows are vertical
        self.Camera_Controls_Frame_2.rowconfigure(index=0, weight=1, minsize=25) 
        self.Camera_Controls_Frame_2.rowconfigure(index=1, weight=1, minsize=1)
        self.Camera_Controls_Frame_2.rowconfigure(index=2, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=3, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=4, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=5, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=6, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=7, weight=1, minsize=25)
        self.Camera_Controls_Frame_2.rowconfigure(index=8, weight=1, minsize=1)
        self.Camera_Controls_Frame_2.rowconfigure(index=9, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=10, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=11, weight=1, minsize=20)
        self.Camera_Controls_Frame_2.rowconfigure(index=12, weight=1, minsize=27)
        self.Camera_Controls_Frame_2.grid(row=0, column=0,  padx=(0,0), pady=(0,0), sticky=N)
        self.Camera_Controls_Frame_2.grid_propagate(0)
        # Birger Frame Camera 2
        self.Birger_Frame_2 = ttk.LabelFrame(self.tab_2, text="Focus Settings", style='Bobwhite.TLabelframe', width=850, height= 110, labelanchor='n')
        self.Birger_Frame_2.columnconfigure(index=0, weight=1, minsize=210)
        self.Birger_Frame_2.columnconfigure(index=1, weight=2, minsize=210)
        self.Birger_Frame_2.columnconfigure(index=2, weight=1, minsize=210)
        self.Birger_Frame_2.columnconfigure(index=3, weight=1, minsize=210)
        self.Birger_Frame_2.grid(row=1, column=0, padx=(0,0), pady=(0,0), sticky=N)
        self.Birger_Frame_2.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Exposure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Exposure Parameters Frame Camera 1
        # Iterator               
        ri_1 = 0
        # Exposure Settings Camera 1
        lbl_ExposureSettings_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Exposure Settings", style="HarlequinThird.TLabel")        
        lbl_ExposureSettings_1.grid(row=ri_1, column=0,columnspan=3, padx=(5,5), pady=(0,0), sticky=W)
        ri_1 = ri_1+1
        # Separator Camera 1
        sep2_1 = ttk.Separator(self.Camera_Controls_Frame_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep2_1.grid(row=ri_1, column=0,columnspan=8, padx=(5,5), pady=(0,3), sticky=E+W)
        ri_1=ri_1+1
        # Exposure Time Parameters Camera 1
        self.lbl_Exposure_Time_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Exposure (s):", anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_Exposure_Time_1.grid(row=ri_1, column=0, columnspan=1,padx=(5,0), pady=(3,3), sticky=E+W)
        self.Entry_UserExposureTime_1 = ttk.Entry(self.Camera_Controls_Frame_1,  style="Harlequin.TEntry", justify='center', textvariable=self.user_exposure_time_1)        
        self.Entry_UserExposureTime_1.grid(row=ri_1, column=1,columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        self.Entry_UserExposureTime_1.insert(0, self.exposure_time_1)
        # Readout Mode Camera 1
        self.lbl_Readout_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Readout Mode:", anchor='e',style="HarlequinFourth.TLabel")
        self.lbl_Readout_1.grid(row=ri_1, column=2, columnspan=1,padx=(5,0), pady=(3,3), sticky=E)        
        self.Combo_Readout_1 = ttk.Combobox(self.Camera_Controls_Frame_1, style="Harlequin.TCombobox", font=('Courier', 18),
                                            justify='center', textvariable = self.user_readout_1)
        self.Combo_Readout_1['values'] = ["1x1", "2x2"]
        self.Combo_Readout_1.grid(row=ri_1, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.readout_1==0:
            self.Combo_Readout_1.set("1x1")
        if self.readout_1 == 1:
            self.Combo_Readout_1.set("2x2")
        self.Combo_Readout_1.option_add('*TCombobox*Listbox.foreground', self.Harlequin_Colors[5])
        self.Combo_Readout_1.option_add('*TCombobox*Listbox.background', self.Harlequin_Colors[1])
        self.Combo_Readout_1.option_add('*TCombobox*Listbox.selectBackground', self.Harlequin_Colors[0])
        self.Combo_Readout_1.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Readout_1.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Readout_1.option_add('*TCombobox*Listbox.justify', 'center')
        #print('elem opt', self.style.element_options("Harlequin.TCombobox.downarrow"))
        ri_1 = ri_1+1
        # Take Series Camera 1
        self.lbl_Take_Series_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Take Series:", anchor='e',  style="HarlequinFourth.TLabel")
        self.lbl_Take_Series_1.grid(row=ri_1, column=0, columnspan=1, padx=(5,0), pady=(3,3), sticky=E)
        self.Entry_UserTakeSeries_1 = ttk.Entry(self.Camera_Controls_Frame_1,style="Harlequin.TEntry",justify='center',textvariable=self.user_series_1)
        self.Entry_UserTakeSeries_1.grid(row=ri_1, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_UserTakeSeries_1.insert(0, 0)
        # Overscan
        self.lbl_Overscan_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Use Overscan:", anchor='e',style="HarlequinFourth.TLabel")
        self.lbl_Overscan_1.grid(row=ri_1, column=2,columnspan=1, padx=(5,0), pady=(3,3), sticky=E)
        self.Overscan_Checkbutton_1 = CustomCheckbutton(self.Camera_Controls_Frame_1, width=212, height=25, callback = self.Overscan_Checkbutton_State_1,
                                                        colors=self.Harlequin_Colors)
        self.Overscan_Checkbutton_1.grid(row=ri_1, column=3, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_1 = ri_1+1
        # Filter Camera 1
        self.lbl_Filter_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Filter:", anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_Filter_1.grid(row=ri_1, column=0,columnspan=1,padx=(5,0), pady=(3,3), sticky=E)        
        self.Combo_Filter_1 = ttk.Combobox(self.Camera_Controls_Frame_1, style="Harlequin.TCombobox", font=('Courier', 18),
                                           justify='center',textvariable = self.user_filter_1)
        self.Combo_Filter_1['values'] = ["None", "H-Alpha", "OI","Continuum"]
        self.Combo_Filter_1.grid(row=ri_1, column=1, columnspan=1,  padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.filter_1==0:
            self.Combo_Filter_1.set("None")
        if self.filter_1 == 1:
            self.Combo_Filter_1.set("H-Alpha")
        if self.filter_1 == 2:
            self.Combo_Filter_1.set("OI")
        if self.filter_1 == 3:
            self.Combo_Filter_1.set("Continuum")
        self.Combo_Filter_1.configure(state='normal')
        self.Combo_Filter_1.option_add('*TCombobox*Listbox.foreground', self.Harlequin_Colors[5])
        self.Combo_Filter_1.option_add('*TCombobox*Listbox.background', self.Harlequin_Colors[1])
        self.Combo_Filter_1.option_add('*TCombobox*Listbox.selectBackground', self.Harlequin_Colors[0])
        self.Combo_Filter_1.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Filter_1.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Filter_1.option_add('*TCombobox*Listbox.justify', 'center')
        # Window Heater
        self.lbl_Window_Heater_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Window Heater:", anchor='e',style="HarlequinFourth.TLabel")
        self.lbl_Window_Heater_1.grid(row=ri_1, column=2,columnspan=1, padx=(5,0), pady=(3,3), sticky=E)
        self.Window_Heater_Checkbutton_1 = CustomCheckbutton(self.Camera_Controls_Frame_1, width=212, height=25, callback = self.Window_Heater_Checkbutton_State_1,
                                                             colors=self.Harlequin_Colors)   
        self.Window_Heater_Checkbutton_1.grid(row=ri_1, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_1 = ri_1+1
        # Frame Type Camera 1
        self.lbl_FrameType_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Frame:", anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_FrameType_1.grid(row=ri_1, column=0,columnspan=1,padx=(5,0), pady=(3,3), sticky=E)        
        self.Combo_Frametype_1 = ttk.Combobox(self.Camera_Controls_Frame_1, style="Harlequin.TCombobox", justify='center',textvariable = self.user_shutter_1)
        self.Combo_Frametype_1['values'] = ["Light", "Dark", "Bias","Flat"]
        self.Combo_Frametype_1.grid(row=ri_1, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.frametype_1==0:
            self.Combo_Frametype_1.set("Light")
        if self.frametype_1 == 1:
            self.Combo_Frametype_1.set("Dark")
        if self.frametype_1 == 2:
            self.Combo_Frametype_1.set("Bias")
        if self.frametype_1 == 3:
            self.Combo_Frametype_1.set("Flat")
        self.Combo_Frametype_1.configure(state='normal')
        self.Combo_Frametype_1.set("Dark")
        self.Combo_Frametype_1.option_add('*TCombobox*Listbox.foreground', self.Harlequin_Colors[5])
        self.Combo_Frametype_1.option_add('*TCombobox*Listbox.background', self.Harlequin_Colors[1])
        self.Combo_Frametype_1.option_add('*TCombobox*Listbox.selectBackground', self.Harlequin_Colors[0])
        self.Combo_Frametype_1.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Frametype_1.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Frametype_1.option_add('*TCombobox*Listbox.justify', 'center')
        # RBI Preflash Parameters Camera 1
        self.lbl_RBI_preflash_duration_1 = ttk.Label(self.Camera_Controls_Frame_1, text="RBI Preflash (s):", anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_RBI_preflash_duration_1.grid(row=ri_1, column=2,columnspan=1, padx=(5,0), pady=(3,3), sticky=E)
        self.Entry_RBI_preflash_duration_1 = ttk.Entry(self.Camera_Controls_Frame_1, justify='center', style="Harlequin.TEntry", textvariable=self.user_preflash_duration_1)
        self.Entry_RBI_preflash_duration_1.grid(row=ri_1, columnspan=1, column=3, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_RBI_preflash_duration_1.insert(0, 0)
        ri_1=ri_1+1
        # Binning Mode Camera 1
        self.lbl_Binning_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Binning Mode:", anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_Binning_1.grid(row=ri_1, column=0, columnspan=1, padx=(5,0), pady=(3,3), sticky=E)        
        self.Combo_Binning_1 = ttk.Combobox(self.Camera_Controls_Frame_1, style="Harlequin.TCombobox", justify='center', textvariable = self.user_binning_1)
        self.Combo_Binning_1['values'] = ["1x1", "2x2", "3x3"]
        self.Combo_Binning_1.grid(row=ri_1, column=1,  columnspan=1,padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.binning_1==0:
            self.Combo_Binning_1.set("1x1")
        if self.binning_1 == 1:
            self.Combo_Binning_1.set("2x2")
        if self.binning_1 == 2:
            self.Combo_Binning_1.set("3x3")
        self.Combo_Binning_1.option_add('*TCombobox*Listbox.foreground', self.Harlequin_Colors[5])
        self.Combo_Binning_1.option_add('*TCombobox*Listbox.background', self.Harlequin_Colors[1])
        self.Combo_Binning_1.option_add('*TCombobox*Listbox.selectBackground', self.Harlequin_Colors[0])
        self.Combo_Binning_1.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Binning_1.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Binning_1.option_add('*TCombobox*Listbox.justify', 'center')
        # Post Flash Flushes Camera 1
        self.lbl_RBI_Flushes_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Post-RBI Flushes:",  anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_RBI_Flushes_1.grid(row=ri_1, column=2, padx=(5,0), columnspan=1, pady=(3,3), sticky=E)
        self.Entry_RBI_Flushes_1 = ttk.Entry(self.Camera_Controls_Frame_1, justify='center', style="Harlequin.TEntry",textvariable=self.user_preflash_clearout_1)
        self.Entry_RBI_Flushes_1.grid(row=ri_1, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_RBI_Flushes_1.insert(0, 0)
        ri_1=ri_1+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Temperature ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.lbl_TempSettings_1 = ttk.Label(self.Camera_Controls_Frame_1, text="Temperature Settings", anchor='nw', style="HarlequinThird.TLabel")
        self.lbl_TempSettings_1.grid(row=ri_1, column=0, columnspan=6, padx=(5,5), pady=(5,0), sticky=W)
        ri_1=ri_1+1
        # Separator Camera 1
        sep2_1 = ttk.Separator(self.Camera_Controls_Frame_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep2_1.grid(row=ri_1, column=0,columnspan=6, padx=(5,5), pady=(0,3), sticky=E+W)
        ri_1=ri_1+1
        # Setpoint parameters Camera 1
        self.lbl_CCD_Setpoint_1 = ttk.Label(self.Camera_Controls_Frame_1, text="CCD Setpoint (\u00b0C):", justify='right', anchor='e',  style="HarlequinFourth.TLabel")
        self.lbl_CCD_Setpoint_1.grid(row=ri_1, column=0, padx=(5,5), pady=(5,3), sticky=E)
        self.Entry_UserSetPoint_1 = ttk.Entry(self.Camera_Controls_Frame_1, style="Harlequin.TEntry", justify='center',textvariable=self.user_set_point_1)
        self.Entry_UserSetPoint_1.grid(row=ri_1, column=1, padx=(5,5), pady=(5,3), sticky=E+W)
        self.Entry_UserSetPoint_1.insert(0, str(self.setpoint_1))
        # CCD Temperature Camera 1
        self.lbl_TemperatureCCD_1 = ttk.Label(self.Camera_Controls_Frame_1, text = "CCD \nTemperature (\u00b0C):", justify='right', anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_TemperatureCCD_1.grid(row=ri_1, column=2, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_DefaultCCDTemp_1 = ttk.Label(self.Camera_Controls_Frame_1, text="--",  borderwidth=3, relief="sunken",anchor='center', style="HarlequinFake.TLabel")
        self.Label_DefaultCCDTemp_1.grid(row=ri_1, column=3, padx=(5,5), pady=(2,2), sticky=E+W)
        ri_1=ri_1+1
        # Recommended CCD Temperature Camera 1
        self.lbl_RecommededCCD_1 = ttk.Label(self.Camera_Controls_Frame_1, text = "Recommended CCD\nTemperature (\u00b0C):",justify='right',anchor='e',  style="HarlequinFourth.TLabel")
        self.lbl_RecommededCCD_1.grid(row=ri_1, column=0, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_RecommendedCCD_1 = ttk.Label(self.Camera_Controls_Frame_1, text="--",  borderwidth=3, relief="sunken",  style="HarlequinFake.TLabel",anchor='center')
        self.Label_RecommendedCCD_1.grid(row=ri_1, column=1,padx=(5,5), pady=(2,2), sticky=E+W)
        # Heat Sink
        self.lbl_HeatSink_1 = ttk.Label(self.Camera_Controls_Frame_1, text = "Heat Sink\nTemperature (\u00b0C):",justify='right', anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_HeatSink_1.grid(row=ri_1, column=2, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_HeatSink_1 = ttk.Label(self.Camera_Controls_Frame_1, text="--", borderwidth=3, relief="sunken",  anchor='center', style="HarlequinFake.TLabel")
        self.Label_HeatSink_1.grid(row=ri_1, column=3,  padx=(5,5), pady=(2,2), sticky=E+W)
        ri_1=ri_1+1
         # Cooling1 Enabled Camera 1
        self.lbl_Cooling1Enabled_1 = ttk.Label(self.Camera_Controls_Frame_1, text = "Cooling Control:",justify='right', anchor='e', style="HarlequinFourth.TLabel")
        self.lbl_Cooling1Enabled_1.grid(row=ri_1, column=0,  padx=(5,5), pady=(2,2), sticky=E)
        self.Label_DefaultCoolingEnabled_1 = ttk.Label(self.Camera_Controls_Frame_1, text="--",  borderwidth=3, relief="sunken", anchor='center',style="HarlequinFake.TLabel")
        self.Label_DefaultCoolingEnabled_1.grid(row=ri_1, column=1,  padx=(5,5), pady=(2,2), sticky=E+W)
        # Cooler Power Camera 1
        self.lbl_Cooler_Power_1 = ttk.Label(self.Camera_Controls_Frame_1, text = "Cooler Power (%):",justify='right',anchor='e',  style="HarlequinFourth.TLabel")
        self.lbl_Cooler_Power_1.grid(row=ri_1, column=2,  padx=(5,5), pady=(2,2), sticky=E)
        self.Label_Cooler_Power_1 = ttk.Label(self.Camera_Controls_Frame_1, text="--",  borderwidth=3, relief="sunken",  style="HarlequinFake.TLabel",anchor='center')
        self.Label_Cooler_Power_1.grid(row=ri_1, column=3, padx=(5,5), pady=(2,2), sticky=E+W)
        ri_1=ri_1+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Buttons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Separator Camera 1
        sep3_1 = ttk.Separator(self.Camera_Controls_Frame_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep3_1.grid(row=ri_1, column=0,columnspan=6, padx=(5,5), pady=(10,3), sticky=E+W)
        ri_1=ri_1+1
        # Buttons Camera 1              
        self.Cool_Button_1 = ttk.Button(self.Camera_Controls_Frame_1, text=" Cool CCD ",  style="HarlequinRaisedButton.TButton",  command=self._cool_CCD_1)
        self.Cool_Button_1.grid(row=ri_1, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Stop Cool Camera 1
        self.Stop_Cooling_1 = ttk.Button(self.Camera_Controls_Frame_1, text=" Stop Cooling ", style="HarlequinRaisedButton.TButton",command = self._stop_cooling_1)
        self.Stop_Cooling_1.grid(row=ri_1, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Expose Camera 1
        self.Exposure_Button_1 = ttk.Button(self.Camera_Controls_Frame_1, text=" Expose ",  style="HarlequinRaisedButton.TButton", command = self._take_exposure_1)
        self.Exposure_Button_1.grid(row=ri_1, column=2, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Abort Exposure Camera 1
        self.Abort_Exposure_Button_1 = ttk.Button(self.Camera_Controls_Frame_1, text=" Abort Exposure ",  style="HarlequinRaisedButton.TButton",  command = self._abort_exposure_1)
        self.Abort_Exposure_Button_1.grid(row=ri_1, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_1=ri_1+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Birger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.Birger_Scrollbar_1 = tk.Scale(self.Birger_Frame_1, from_=0, to=25000, orient=HORIZONTAL, showvalue=1, resolution=1, variable=self.birger_scale_setpoint_1,
                                           troughcolor=self.Harlequin_Colors[1], background=self.Harlequin_Colors[0], foreground=self.Harlequin_Colors[6],
                                           activebackground=self.Harlequin_Colors[5], relief='flat', bd=0, font=('Courier', 18))
        self.Birger_Scrollbar_1.grid(row=0, column=0, columnspan=4, padx=(5,5), pady=(0,3), sticky=E+W)        
        # Autofocus Camera 1
        self.Autofocus_Button_1 = ttk.Button(self.Birger_Frame_1, text="Autofocus", style="HarlequinRaisedButton.TButton",  command=None)
        self.Autofocus_Button_1.grid(row=1, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        # GoTo Button Camera 1
        self.GoTo_Button_1 = ttk.Button(self.Birger_Frame_1, text = 'Go To Setpoint', style="HarlequinRaisedButton.TButton",  command=self._birger_goto_1)
        self.GoTo_Button_1.grid(row=1, column=2, padx=(5,5), pady=(3,3), sticky=E+W)
        # GoTo Entry Camera 1
        self.Entry_GoTo_1 = ttk.Entry(self.Birger_Frame_1, style="Harlequin.TEntry", justify='right',textvariable=self.birger_entry_setpoint_1)
        self.Entry_GoTo_1.grid(row=1, column=3, padx=(5,5), pady=(3,3), sticky=E+W)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Exposure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Exposure Parameters Frame Camera 1
        # Iterator               
        ri_2 = 0
        # Exposure Settings Camera 1
        lbl_ExposureSettings_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Exposure Settings", style="BobwhiteThird.TLabel")        
        lbl_ExposureSettings_2.grid(row=ri_2, column=0,columnspan=3, padx=(5,5), pady=(0,0), sticky=W)
        ri_2 = ri_2+1
        # Separator Camera 1
        sep2_2 = ttk.Separator(self.Camera_Controls_Frame_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep2_2.grid(row=ri_2, column=0,columnspan=8, padx=(5,5), pady=(0,3), sticky=E+W)
        ri_2=ri_2+1
        # Exposure Time Parameters Camera 1
        self.lbl_Exposure_Time_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Exposure (s):", anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_Exposure_Time_2.grid(row=ri_2, column=0, columnspan=1,padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_UserExposureTime_2 = ttk.Entry(self.Camera_Controls_Frame_2,  style="Bobwhite.TEntry", justify='center', textvariable=self.user_exposure_time_2)
        
        self.Entry_UserExposureTime_2.grid(row=ri_2, column=1,columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        self.Entry_UserExposureTime_2.insert(0, str(self.exposure_time_2))
        # Readout Mode Camera 1
        self.lbl_Readout_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Readout Mode:", anchor='e',style="BobwhiteFourth.TLabel")
        self.lbl_Readout_2.grid(row=ri_2, column=2, columnspan=1,padx=(5,5), pady=(3,3), sticky=E)        
        self.Combo_Readout_2 = ttk.Combobox(self.Camera_Controls_Frame_2, style="Bobwhite.TCombobox", font=('Courier', 18),
                                            justify='center', textvariable = self.user_readout_2)
        self.Combo_Readout_2['values'] = ["1x1", "2x2"]
        self.Combo_Readout_2.grid(row=ri_2, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.readout_2==0:
            self.Combo_Readout_2.set("1x1")
        if self.readout_2 == 1:
            self.Combo_Readout_2.set("2x2")
        self.Combo_Readout_2.option_add('*TCombobox*Listbox.foreground', self.Bobwhite_Colors[5])
        self.Combo_Readout_2.option_add('*TCombobox*Listbox.background', self.Bobwhite_Colors[1])
        self.Combo_Readout_2.option_add('*TCombobox*Listbox.selectBackground', self.Bobwhite_Colors[0])
        self.Combo_Readout_2.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Readout_2.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Readout_2.option_add('*TCombobox*Listbox.justify', 'center')
        ri_2 = ri_2+1
        # Take Series Camera 1
        self.lbl_Take_Series_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Take Series:", anchor='e',  style="BobwhiteFourth.TLabel")
        self.lbl_Take_Series_2.grid(row=ri_2, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E)
        self.Entry_UserTakeSeries_2 = ttk.Entry(self.Camera_Controls_Frame_2,style="Bobwhite.TEntry",justify='center',textvariable=self.user_series_2)
        self.Entry_UserTakeSeries_2.grid(row=ri_2, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_UserTakeSeries_2.insert(0, str(0))
        # Overscan
        self.lbl_Overscan_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Use Overscan:", anchor='e',style="BobwhiteFourth.TLabel")
        self.lbl_Overscan_2.grid(row=ri_2, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=E)
        self.Overscan_Checkbutton_2 = CustomCheckbutton(self.Camera_Controls_Frame_2, width=212, height=25, callback = self.Overscan_Checkbutton_State_2,
                                                        colors=self.Bobwhite_Colors)
        self.Overscan_Checkbutton_2.grid(row=ri_2, column=3, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_2 = ri_2+1
        # Filter Camera 1
        self.lbl_Filter_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Filter:", anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_Filter_2.grid(row=ri_2, column=0,columnspan=1,padx=(5,5), pady=(3,3), sticky=E)        
        self.Combo_Filter_2 = ttk.Combobox(self.Camera_Controls_Frame_2, style="Bobwhite.TCombobox", font=('Courier', 18),
                                           justify='center',textvariable = self.user_filter_2)
        self.Combo_Filter_2['values'] = ["None", "H-Alpha", "OI","Continuum"]
        self.Combo_Filter_2.grid(row=ri_2, column=1, columnspan=1,  padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.filter_2==0:
            self.Combo_Filter_2.set("None")
        if self.filter_2 == 1:
            self.Combo_Filter_2.set("H-Alpha")
        if self.filter_2 == 2:
            self.Combo_Filter_2.set("OI")
        if self.filter_2 == 3:
            self.Combo_Filter_2.set("Continuum")
        self.Combo_Filter_2.configure(state='normal')
        self.Combo_Filter_2.option_add('*TCombobox*Listbox.foreground', self.Bobwhite_Colors[5])
        self.Combo_Filter_2.option_add('*TCombobox*Listbox.background', self.Bobwhite_Colors[1])
        self.Combo_Filter_2.option_add('*TCombobox*Listbox.selectBackground', self.Bobwhite_Colors[0])
        self.Combo_Filter_2.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Filter_2.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Filter_2.option_add('*TCombobox*Listbox.justify', 'center')
        # Window Heater
        self.lbl_Window_Heater_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Window Heater:", anchor='e',style="BobwhiteFourth.TLabel")
        self.lbl_Window_Heater_2.grid(row=ri_2, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=E)
        self.Window_Heater_Checkbutton_2 = CustomCheckbutton(self.Camera_Controls_Frame_2, width=212, height=25, callback = self.Window_Heater_Checkbutton_State_2,
                                                             colors=self.Bobwhite_Colors)   
        self.Window_Heater_Checkbutton_2.grid(row=ri_2, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_2 = ri_2+1
        # Frame Type Camera 1
        self.lbl_FrameType_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Frame:", anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_FrameType_2.grid(row=ri_2, column=0,columnspan=1,padx=(5,5), pady=(3,3), sticky=E)        
        self.Combo_Frametype_2 = ttk.Combobox(self.Camera_Controls_Frame_2, style="Bobwhite.TCombobox", justify='center',textvariable = self.user_shutter_2)
        self.Combo_Frametype_2['values'] = ["Light", "Dark", "Bias","Flat"]
        self.Combo_Frametype_2.grid(row=ri_2, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.frametype_2==0:
            self.Combo_Frametype_2.set("Light")
        if self.frametype_2 == 1:
            self.Combo_Frametype_2.set("Dark")
        if self.frametype_2 == 2:
            self.Combo_Frametype_2.set("Bias")
        if self.frametype_2 == 3:
            self.Combo_Frametype_2.set("Flat")
        self.Combo_Frametype_2.configure(state='normal')
        self.Combo_Frametype_2.set("Dark")
        self.Combo_Frametype_2.option_add('*TCombobox*Listbox.foreground', self.Bobwhite_Colors[5])
        self.Combo_Frametype_2.option_add('*TCombobox*Listbox.background', self.Bobwhite_Colors[1])
        self.Combo_Frametype_2.option_add('*TCombobox*Listbox.selectBackground', self.Bobwhite_Colors[0])
        self.Combo_Frametype_2.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Frametype_2.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Frametype_2.option_add('*TCombobox*Listbox.justify', 'center')
        # RBI Preflash Parameters Camera 1
        self.lbl_RBI_preflash_duration_2 = ttk.Label(self.Camera_Controls_Frame_2, text="RBI Preflash (s):", anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_RBI_preflash_duration_2.grid(row=ri_2, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=E)
        self.Entry_RBI_preflash_duration_2 = ttk.Entry(self.Camera_Controls_Frame_2, justify='center', style="Bobwhite.TEntry", textvariable=self.user_preflash_duration_2)
        self.Entry_RBI_preflash_duration_2.grid(row=ri_2, columnspan=1, column=3, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_RBI_preflash_duration_2.insert(0, str(0))
        ri_2=ri_2+1
        # Binning Mode Camera 1
        self.lbl_Binning_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Binning Mode:", anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_Binning_2.grid(row=ri_2, column=0, columnspan=1, padx=(0,3), pady=(3,3), sticky=E)        
        self.Combo_Binning_2 = ttk.Combobox(self.Camera_Controls_Frame_2, style="Bobwhite.TCombobox", justify='center', textvariable = self.user_binning_2)
        self.Combo_Binning_2['values'] = ["1x1", "2x2", "3x3"]
        self.Combo_Binning_2.grid(row=ri_2, column=1,  columnspan=1,padx=(5,5), pady=(3,3), sticky=E+W)        
        if self.binning_2==0:
            self.Combo_Binning_2.set("1x1")
        if self.binning_2 == 1:
            self.Combo_Binning_2.set("2x2")
        if self.binning_2 == 2:
            self.Combo_Binning_2.set("3x3")
        self.Combo_Binning_2.option_add('*TCombobox*Listbox.foreground', self.Bobwhite_Colors[5])
        self.Combo_Binning_2.option_add('*TCombobox*Listbox.background', self.Bobwhite_Colors[1])
        self.Combo_Binning_2.option_add('*TCombobox*Listbox.selectBackground', self.Bobwhite_Colors[0])
        self.Combo_Binning_2.option_add('*TCombobox*Listbox.font', ('Courier', 18))
        self.Combo_Binning_2.option_add('*TCombobox.font', ('Courier', 18))
        self.Combo_Binning_2.option_add('*TCombobox*Listbox.justify', 'center')
        # Post Flash Flushes Camera 1
        self.lbl_RBI_Flushes_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Post-RBI Flushes:",  anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_RBI_Flushes_2.grid(row=ri_2, column=2, padx=(5,5), columnspan=1, pady=(3,3), sticky=E)
        self.Entry_RBI_Flushes_2 = ttk.Entry(self.Camera_Controls_Frame_2, justify='center', style="Bobwhite.TEntry",textvariable=self.user_preflash_clearout_2)
        self.Entry_RBI_Flushes_2.grid(row=ri_2, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        self.Entry_RBI_Flushes_2.insert(0, str(0))
        ri_2=ri_2+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Temperature ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.lbl_TempSettings_2 = ttk.Label(self.Camera_Controls_Frame_2, text="Temperature Settings", anchor='nw', style="BobwhiteThird.TLabel")
        self.lbl_TempSettings_2.grid(row=ri_2, column=0, columnspan=6, padx=(5,5), pady=(5,0), sticky=W)
        ri_2=ri_2+1
        # Separator Camera 1
        sep2_2 = ttk.Separator(self.Camera_Controls_Frame_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep2_2.grid(row=ri_2, column=0,columnspan=6, padx=(5,5), pady=(0,3), sticky=E+W)
        ri_2=ri_2+1
        # Setpoint parameters Camera 1
        self.lbl_CCD_Setpoint_2 = ttk.Label(self.Camera_Controls_Frame_2, text="CCD Setpoint (\u00b0C):", justify='right', anchor='e',  style="BobwhiteFourth.TLabel")
        self.lbl_CCD_Setpoint_2.grid(row=ri_2, column=0, padx=(5,5), pady=(5,3), sticky=E)
        self.Entry_UserSetPoint_2 = ttk.Entry(self.Camera_Controls_Frame_2, style="Bobwhite.TEntry", justify='center',textvariable=self.user_set_point_2)
        self.Entry_UserSetPoint_2.grid(row=ri_2, column=1, columnspan=1, padx=(5,5), pady=(5,3), sticky=E+W)
        self.Entry_UserSetPoint_2.insert(0, str(self.setpoint_2))
        # CCD Temperature Camera 1
        self.lbl_TemperatureCCD_2 = ttk.Label(self.Camera_Controls_Frame_2, text = "CCD Temperature (\u00b0C):", justify='right', anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_TemperatureCCD_2.grid(row=ri_2, column=2, columnspan=1, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_DefaultCCDTemp_2 = ttk.Label(self.Camera_Controls_Frame_2, text="--",  borderwidth=3, relief="sunken",anchor='center', style="BobwhiteFake.TLabel")
        self.Label_DefaultCCDTemp_2.grid(row=ri_2, column=3, columnspan=1, padx=(5,5), pady=(2,2), sticky=E+W)
        ri_2=ri_2+1
        # Recommended CCD Temperature Camera 1
        self.lbl_RecommededCCD_2 = ttk.Label(self.Camera_Controls_Frame_2, text = "Recommended CCD \nTemperature (\u00b0C):",justify='right',anchor='e',  style="BobwhiteFourth.TLabel")
        self.lbl_RecommededCCD_2.grid(row=ri_2, column=0, columnspan=1, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_RecommendedCCD_2 = ttk.Label(self.Camera_Controls_Frame_2, text="--",  borderwidth=3, relief="sunken",  style="BobwhiteFake.TLabel",anchor='center')
        self.Label_RecommendedCCD_2.grid(row=ri_2, column=1,columnspan=1,padx=(5,5), pady=(2,2), sticky=E+W)
        # Heat Sink
        self.lbl_HeatSink_2 = ttk.Label(self.Camera_Controls_Frame_2, text = "Heat Sink \nTemperature (\u00b0C):",justify='right', anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_HeatSink_2.grid(row=ri_2, column=2, columnspan=1, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_HeatSink_2 = ttk.Label(self.Camera_Controls_Frame_2, text="--", borderwidth=3, relief="sunken",  anchor='center', style="BobwhiteFake.TLabel")
        self.Label_HeatSink_2.grid(row=ri_2, column=3, columnspan=1, padx=(5,5), pady=(2,2), sticky=E+W)
        ri_2=ri_2+1
         # Cooling1 Enabled Camera 1
        self.lbl_Cooling1Enabled_2 = ttk.Label(self.Camera_Controls_Frame_2, text = "Cooling Control:",justify='right', anchor='e', style="BobwhiteFourth.TLabel")
        self.lbl_Cooling1Enabled_2.grid(row=ri_2, column=0, columnspan=1, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_DefaultCoolingEnabled_2 = ttk.Label(self.Camera_Controls_Frame_2, text="--",  borderwidth=3, relief="sunken", anchor='center',style="BobwhiteFake.TLabel")
        self.Label_DefaultCoolingEnabled_2.grid(row=ri_2, column=1, columnspan=1, padx=(5,5), pady=(2,2), sticky=E+W)
        # Cooler Power Camera 1
        self.lbl_Cooler_Power_2 = ttk.Label(self.Camera_Controls_Frame_2, text = "Cooler Power (%):",justify='right',anchor='e',  style="BobwhiteFourth.TLabel")
        self.lbl_Cooler_Power_2.grid(row=ri_2, column=2, columnspan=1, padx=(5,5), pady=(2,2), sticky=E)
        self.Label_Cooler_Power_2 = ttk.Label(self.Camera_Controls_Frame_2, text="--",  borderwidth=3, relief="sunken",  style="BobwhiteFake.TLabel",anchor='center')
        self.Label_Cooler_Power_2.grid(row=ri_2, column=3,columnspan=1,padx=(5,5), pady=(2,2), sticky=E+W)
        ri_2=ri_2+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Buttons ~~~~~~~~~~~~~~!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Separator Camera 1
        sep3_2 = ttk.Separator(self.Camera_Controls_Frame_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep3_2.grid(row=ri_2, column=0,columnspan=6, padx=(5,5), pady=(10,3), sticky=E+W)
        ri_2=ri_2+1
        # Buttons Camera 1              
        self.Cool_Button_2 = ttk.Button(self.Camera_Controls_Frame_2, text=" Cool CCD ",  style="BobwhiteRaisedButton.TButton",  command=self._cool_CCD_2)
        self.Cool_Button_2.grid(row=ri_2, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Stop Cool Camera 1
        self.Stop_Cooling_2 = ttk.Button(self.Camera_Controls_Frame_2, text=" Stop Cooling ", style="BobwhiteRaisedButton.TButton",command = self._stop_cooling_2)
        self.Stop_Cooling_2.grid(row=ri_2, column=1, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Expose Camera 1
        self.Exposure_Button_2 = ttk.Button(self.Camera_Controls_Frame_2, text=" Expose ",  style="BobwhiteRaisedButton.TButton", command = self._take_exposure_2)
        self.Exposure_Button_2.grid(row=ri_2, column=2, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        # Abort Exposure Camera 1
        self.Abort_Exposure_Button_2 = ttk.Button(self.Camera_Controls_Frame_2, text=" Abort Exposure ",  style="BobwhiteRaisedButton.TButton",  command = self._abort_exposure_2)
        self.Abort_Exposure_Button_2.grid(row=ri_2, column=3, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)
        ri_2=ri_2+1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Birger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.Birger_Scrollbar_2 = tk.Scale(self.Birger_Frame_2, from_=0, to=25000, orient=HORIZONTAL, showvalue=1, resolution=1, variable=self.birger_scale_setpoint_2,
                                           troughcolor=self.Bobwhite_Colors[1], background=self.Bobwhite_Colors[0], foreground=self.Bobwhite_Colors[6],
                                           activebackground=self.Bobwhite_Colors[5], relief='flat', bd=0, font=('Courier', 18))
        self.Birger_Scrollbar_2.grid(row=0, column=0, columnspan=4, padx=(5,5), pady=(0,3), sticky=E+W)        
        # Autofocus Camera 1
        self.Autofocus_Button_2 = ttk.Button(self.Birger_Frame_2, text="Autofocus", style="BobwhiteRaisedButton.TButton",  command=None)
        self.Autofocus_Button_2.grid(row=1, column=0, columnspan=1, padx=(5,5), pady=(3,3), sticky=E+W)        
        # GoTo Button Camera 1
        self.GoTo_Button_2 = ttk.Button(self.Birger_Frame_2, text = 'Go To Setpoint', style="BobwhiteRaisedButton.TButton",  command=self._birger_goto_2)
        self.GoTo_Button_2.grid(row=1, column=2, padx=(5,5), pady=(3,3), sticky=E+W)
        # GoTo Entry Camera 1
        self.Entry_GoTo_2 = ttk.Entry(self.Birger_Frame_2, style="Bobwhite.TEntry", justify='right',textvariable=self.birger_entry_setpoint_2)
        self.Entry_GoTo_2.grid(row=1, column=3, padx=(5,5), pady=(3,3), sticky=E+W)   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Right-Hand-Side Canvas Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.Canvas_Frame = ttk.Frame(self.Main_Frame,  style='Common.TFrame')
        self.Canvas_Frame.grid(row=0, column=1, rowspan=3,  padx=(5,5), pady=(0,0), sticky=N)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin DS9 Canvas Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.Canvas_Label_Frame_1 = ttk.Frame(self.Canvas_Frame, width=1050)
        self.Canvas_Label_Frame_1.grid(row=0, column=0, sticky=N, padx=(5,5), pady=(0,0))
        # DS9 Imitation Frame
        self.Vertical_Harlequin_Label = ttk.Label(self.Canvas_Label_Frame_1, text="Harlequin Status: Disconnected",  style="HarlequinThird.TLabel")
        self.DS9_Frame_1 = ttk.LabelFrame(self.Canvas_Label_Frame_1, labelwidget=self.Vertical_Harlequin_Label, style='Harlequin.TLabelframe',
                                          labelanchor='n', width=1060, height=500)
        self.DS9_Frame_1.columnconfigure(index=0, weight=1, minsize=150)
        self.DS9_Frame_1.columnconfigure(index=1, weight=1, minsize=680)
        self.DS9_Frame_1.columnconfigure(index=2, weight=1, minsize=190)
        self.DS9_Frame_1.grid(row=0, column=0, padx=(0,0), pady=(3,3), sticky=E+W)
        self.DS9_Frame_1.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin DS9 Button Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.DS9_Button_Frame_1 =  ttk.Frame(self.DS9_Frame_1, style='Harlequin.TFrame')
        self.DS9_Button_Frame_1.grid(row=0, column=0, padx=(0,0), pady=(2,2), sticky=N)
        # Open_file
        self.Open_File_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Open File ",  style="HarlequinRaisedButton.TButton", width = 10, command = self.open_file_1)
        self.Open_File_Button_1.grid(row=0, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
        # Zoom
        self.Zoom_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Zoom ",  style="HarlequinRaisedButton.TButton", width = 10, command = self.show_zoom_options_1)
        self.Zoom_Button_1.grid(row=1, column=0, columnspan=2,rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
        # Scale
        self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", width = 10, command = self.show_scale_options_1)
        self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
        # IRAF
        self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",  style="HarlequinRaisedButton.TButton", width = 10, command = self.show_aperphot_options_1)
        self.Aperphot_Button_1.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin DS9 Canvas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #      
        self.Canvas_1 = tk.Canvas(self.DS9_Frame_1, bg="black", borderwidth=1, width=675, height=450, bd=0, highlightcolor='black', highlightbackground=self.Harlequin_Colors[0],
                                  relief="sunken", highlightthickness=1) 
        self.Canvas_1.bind('<MouseWheel>', self.mouse_zoom_1)
        self.Canvas_1.grid(row=0, column=1,  padx=(3,3), pady=(3,3), sticky=E+W)        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin Ginga ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #       
        self.fi_1 = ImageViewCanvas(self.logger)
        self.fi_1.set_widget(self.Canvas_1)        
        self.fi_1.enable_autocuts('on')
        self.fi_1.set_autocut_params('zscale')
        self.fi_1.enable_autozoom('on')
        self.fi_1.enable_draw(False)
        self.fi_1.set_enter_focus(True)
        self.fi_1.set_callback('cursor-changed', self.cursor_cb_1)        
        self.fi_1.set_bg(0.2, 0.2, 0.2)
        self.fi_1.ui_set_active(True)
        self.fi_1.show_pan_mark(True)
        self.fitsimage_1 = self.fi_1   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Harlequin DS9 Info Panel ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.DS9_Info_Panel_1 = ttk.Frame(self.DS9_Frame_1, style='Harlequin.TFrame')
        self.DS9_Info_Panel_1.grid(row=0, column=2, padx=(0,0), pady=(0,0), sticky=N)
        # Info Label
        self.Info_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Statistics ", style="HarlequinThird.TLabel")
        self.Info_Label_1.grid(row=0, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)        
        sep_info_1 = ttk.Separator(self.DS9_Info_Panel_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep_info_1.grid(row=1, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
        # Min
        self.Mean_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Mean: ", style="HarlequinSmall.TLabel")
        self.Mean_Label_1.grid(row=2, column=2,columnspan=1, padx=(0,0), pady=(0,0), sticky=E+W)
        self.Mean_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.Mean_1.grid(row=2, column=3,columnspan=1, padx=(0,0), pady=(0,0), sticky=E+W)
        # StdDev
        self.StdDev_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="StdDev: ", style="HarlequinSmall.TLabel")
        self.StdDev_Label_1.grid(row=3, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.StdDev_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.StdDev_1.grid(row=3, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Min
        self.Min_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Min: ", style="HarlequinSmall.TLabel")
        self.Min_Label_1.grid(row=4, column=2, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Min_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.Min_1.grid(row=4, column=3, padx=(0,0), pady=(3,3), sticky=E+W)
        # Max
        self.Max_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Max: ", style="HarlequinSmall.TLabel")
        self.Max_Label_1.grid(row=5, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Max_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.Max_1.grid(row=5, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Current Value
        self.Value_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Pixel Data ", style="HarlequinThird.TLabel")
        self.Value_Label_1.grid(row=6, column=2,columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
        sep_info_1 = ttk.Separator(self.DS9_Info_Panel_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep_info_1.grid(row=7, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
        # X Pixel
        self.X_Pixel_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="X: ", style="HarlequinSmall.TLabel")        
        self.X_Pixel_Label_1.grid(row=8, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.X_Pixel_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel",  anchor='w')        
        self.X_Pixel_1.grid(row=8, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Y Pixel        
        self.Y_Pixel_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Y: ", style="HarlequinSmall.TLabel")
        self.Y_Pixel_Label_1.grid(row=9, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Y_Pixel_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.Y_Pixel_1.grid(row=9, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Value Pixel        
        self.Value_Pixel_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Value: ", style="HarlequinSmall.TLabel")
        self.Value_Pixel_Label_1.grid(row=10, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Value_Pixel_1 = ttk.Label(self.DS9_Info_Panel_1, text=" -- ", style="HarlequinSmall.TLabel")
        self.Value_Pixel_1.grid(row=10, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite DS9 Canvas Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Camera 2 Canvas Frame
        self.Canvas_Label_Frame_2 = ttk.Frame(self.Canvas_Frame, width=1050)
        self.Canvas_Label_Frame_2.grid(row=1, column=0, sticky=N, padx=(5,5), pady=(0,0))
        # DS9 Imitation Frame
        self.Vertical_Bobwhite_Label = ttk.Label(self.Canvas_Label_Frame_2, text="Bobwhite Status: Disconnected",  style="BobwhiteThird.TLabel")
        self.DS9_Frame_2 = ttk.LabelFrame(self.Canvas_Label_Frame_2, labelwidget=self.Vertical_Bobwhite_Label, style='Bobwhite.TLabelframe',
                                          labelanchor='n', width=1060, height=500)
        self.DS9_Frame_2.columnconfigure(index=0, weight=1, minsize=150)
        self.DS9_Frame_2.columnconfigure(index=1, weight=1, minsize=680)
        self.DS9_Frame_2.columnconfigure(index=2, weight=1, minsize=190)
        self.DS9_Frame_2.grid(row=0, column=0, padx=(0,0), pady=(3,3), sticky=E+W)
        self.DS9_Frame_2.grid_propagate(0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite DS9 Button Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.DS9_Button_Frame_2 =  ttk.Frame(self.DS9_Frame_2, style='Bobwhite.TFrame')
        self.DS9_Button_Frame_2.grid(row=0, column=0, padx=(0,0), pady=(2,2), sticky=N)
        # Open_file
        self.Open_File_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Open File ",  style="BobwhiteRaisedButton.TButton", width = 10, command = self.open_file_2)
        self.Open_File_Button_2.grid(row=0, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
        # Zoom
        self.Zoom_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Zoom ",  style="BobwhiteRaisedButton.TButton", width = 10, command = self.show_zoom_options_2)
        self.Zoom_Button_2.grid(row=1, column=0, columnspan=2,rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
        # Scale
        self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteRaisedButton.TButton", width = 10, command = self.show_scale_options_2)
        self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
        # IRAF
        self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",  style="BobwhiteRaisedButton.TButton", width = 10, command = self.show_aperphot_options_2)
        self.Aperphot_Button_2.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite DS9 Canvas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #     
        self.Canvas_2 = tk.Canvas(self.DS9_Frame_2, bg="black", borderwidth=1, width=675, height=450, bd=0, highlightcolor='black', highlightbackground=self.Bobwhite_Colors[0],
                                  relief="sunken", highlightthickness=1) 
        self.Canvas_2.bind('<MouseWheel>', self.mouse_zoom_2)
        self.Canvas_2.grid(row=0, column=1,  padx=(3,3), pady=(3,3), sticky=E+W)        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite Ginga ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #     
        self.fi_2 = ImageViewCanvas(self.logger)
        self.fi_2.set_widget(self.Canvas_2)        
        self.fi_2.enable_autocuts('on')
        self.fi_2.set_autocut_params('zscale')
        self.fi_2.enable_autozoom('on')
        self.fi_2.enable_draw(False)
        self.fi_2.set_enter_focus(True)
        self.fi_2.set_callback('cursor-changed', self.cursor_cb_2)        
        self.fi_2.set_bg(0.2, 0.2, 0.2)
        self.fi_2.ui_set_active(True)
        self.fi_2.show_pan_mark(True)
        self.fitsimage_2 = self.fi_2   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bobwhite DS9 Info Panel ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.DS9_Info_Panel_2 = ttk.Frame(self.DS9_Frame_2, style='Bobwhite.TFrame')
        self.DS9_Info_Panel_2.grid(row=0, column=2, padx=(0,0), pady=(0,0), sticky=N)
        # Info Label
        self.Info_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Statistics ", style="BobwhiteThird.TLabel")
        self.Info_Label_2.grid(row=0, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)        
        sep_info_2 = ttk.Separator(self.DS9_Info_Panel_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep_info_2.grid(row=1, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
        # Min
        self.Mean_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Mean: ", style="BobwhiteSmall.TLabel")
        self.Mean_Label_2.grid(row=2, column=2,columnspan=1, padx=(0,0), pady=(0,0), sticky=E+W)
        self.Mean_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.Mean_2.grid(row=2, column=3,columnspan=1, padx=(0,0), pady=(0,0), sticky=E+W)
        # StdDev
        self.StdDev_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="StdDev: ", style="BobwhiteSmall.TLabel")
        self.StdDev_Label_2.grid(row=3, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.StdDev_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.StdDev_2.grid(row=3, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Min
        self.Min_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Min: ", style="BobwhiteSmall.TLabel")
        self.Min_Label_2.grid(row=4, column=2, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Min_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.Min_2.grid(row=4, column=3, padx=(0,0), pady=(3,3), sticky=E+W)
        # Max
        self.Max_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Max: ", style="BobwhiteSmall.TLabel")
        self.Max_Label_2.grid(row=5, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Max_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.Max_2.grid(row=5, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Current Value
        self.Value_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Pixel Data ", style="BobwhiteThird.TLabel")
        self.Value_Label_2.grid(row=6, column=2,columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
        sep_info_2 = ttk.Separator(self.DS9_Info_Panel_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep_info_2.grid(row=7, column=2,columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
        # X Pixel
        self.X_Pixel_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="X: ", style="BobwhiteSmall.TLabel")        
        self.X_Pixel_Label_2.grid(row=8, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.X_Pixel_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel",  anchor='w')        
        self.X_Pixel_2.grid(row=8, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Y Pixel        
        self.Y_Pixel_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Y: ", style="BobwhiteSmall.TLabel")
        self.Y_Pixel_Label_2.grid(row=9, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Y_Pixel_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.Y_Pixel_2.grid(row=9, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        # Value Pixel        
        self.Value_Pixel_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Value: ", style="BobwhiteSmall.TLabel")
        self.Value_Pixel_Label_2.grid(row=10, column=2,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W)
        self.Value_Pixel_2 = ttk.Label(self.DS9_Info_Panel_2, text=" -- ", style="BobwhiteSmall.TLabel")
        self.Value_Pixel_2.grid(row=10, column=3,columnspan=1, padx=(0,0), pady=(3,3), sticky=E+W) 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Start Program ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self._init_cameras()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Start/Stop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def _init_cameras(self):
        self.running = True
        self.camera_thread = Camera_Thread.CameraThreadedClient(self.Camera_Queue_In, self.Camera_Queue_Out)
        self.Camera_Queue_In.put(["INIT", None])
        self.camera_thread.start()
        self._camera_talker()

    def _on_close(self):
        self._abort_all()
        self._stop_cooling_all()
        quit_command = 'NNNNNNNNNNNNNNNN~QUIT~'
        self.Camera_Queue_In.put(["QUIT", quit_command])
        self.master.destroy()
       # sys.exit()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GUI States ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def tab_changed(self, event):
        #print(self.tab_parent.select())  # get the instance of tab
        #print(self.tab_parent.index(self.tab_parent.select()))  # get the index of the tab. Bobwhite_Colors
        tab_index = self.tab_parent.index(self.tab_parent.select())
        if tab_index == 0:
            # Change Style To Harlequin
            self.style.configure("TNotebook",  bd=3, bordercolor = self.Harlequin_Colors[4], background=self.Harlequin_Colors[0],
                                 lightcolor=self.Harlequin_Colors[4], darkcolor=self.Harlequin_Colors[4])
            self.style.configure("TNotebook.Tab", font=("Courier", "24"), borderwidth=3, justify="center")   
            self.style.map("TNotebook.Tab",
                           relief=[("selected", "raised"), ("!selected", "sunken"),],
                           background=[("selected", self.Harlequin_Colors[0]), ("!selected", self.Bobwhite_Colors[0])],
                           foreground=[("selected", self.Harlequin_Colors[5]), ("!selected", self.Bobwhite_Colors[4])],
                           borderwidth=[("selected", 3), ("!selected", 3)],
                           bordercolor=[("selected", self.Harlequin_Colors[5]), ("!selected", self.Bobwhite_Colors[5])],
                           highlightcolor=[("selected", self.Harlequin_Colors[2]), ("!selected", self.Bobwhite_Colors[1])],
                           highlightthickness=[("selected", 3), ("!selected", 0)],
                           lightcolor = [("selected", self.Harlequin_Colors[4]), ("!selected", self.Bobwhite_Colors[4])],
                           darkcolor = [("selected", self.Harlequin_Colors[4]), ("!selected", self.Bobwhite_Colors[4])])            
        elif tab_index == 1:
            # Change Notebook Style to Bobwhite
            self.style.configure("TNotebook",  bd=3, bordercolor = self.Bobwhite_Colors[4], background=self.Bobwhite_Colors[0],
                                 lightcolor=self.Bobwhite_Colors[4], darkcolor=self.Bobwhite_Colors[4])
            self.style.configure("TNotebook.Tab", font=("Courier", "24"), borderwidth=3, highlightthickness=3, justify="center")   
            self.style.map("TNotebook.Tab",
                           relief=[("selected", "raised"), ("!selected", "sunken"),],
                           background=[("selected", self.Bobwhite_Colors[0]), ("!selected", self.Harlequin_Colors[0])],
                           foreground=[("selected", self.Bobwhite_Colors[5]), ("!selected", self.Harlequin_Colors[4])],
                           borderwidth=[("selected", 3), ("!selected", 3)],
                           bordercolor=[("selected", self.Bobwhite_Colors[5]), ("!selected", self.Harlequin_Colors[5])],
                           highlightcolor=[("selected", self.Bobwhite_Colors[2]), ("!selected", self.Harlequin_Colors[1])],
                           highlightthickness=[("selected", 3), ("!selected", 0)],
                           lightcolor = [("selected", self.Bobwhite_Colors[4]), ("!selected", self.Harlequin_Colors[4])],
                           darkcolor = [("selected", self.Bobwhite_Colors[4]), ("!selected", self.Harlequin_Colors[4])])
            
    def Harlequin_Widget_Flash(self, times, widget):
        if widget['style'] == "Harlequin.TEntry":
            widget['style'] = "Error.TEntry"
        else:
            widget['style'] = "Harlequin.TEntry"
        times = times - 1
        if times > 0:
            widget.after(100, lambda t=times: self.Harlequin_Widget_Flash(t, widget))
        else:
            widget['style'] = "Harlequin.TEntry"

    def Bobwhite_Widget_Flash(self, times, widget):
        if widget['style'] == "Bobwhite.TEntry":
            widget['style'] = "Error.TEntry"
        else:
            widget['style'] = "Bobwhite.TEntry"
        times = times - 1
        if times > 0:
            widget.after(100, lambda t=times: self.Bobwhite_Widget_Flash(t, widget))
        else:
            widget['style'] = "Bobwhite.TEntry"
            
    def Overscan_Checkbutton_State_1(self):
        if self.overscan_1 == 0:
            self.overscan_1 = 1
        elif self.overscan_1 == 1:
            self.overscan_1 = 0
        else:
            pass
        return self.overscan_1

    def Overscan_Checkbutton_State_2(self):
        current_state = self.user_overscan_2.get()
        if current_state == 1:
            self.Overscan_Checkbutton_2['text'] = "On"
            self.Overscan_Checkbutton_2['borderwidth'] = 3
            self.Overscan_Checkbutton_2['foreground'] = '#FF3864'
            self.Overscan_Checkbutton_2['relief'] = 'sunken'
        else:
            self.Overscan_Checkbutton_2['text'] = "Off"
            self.Overscan_Checkbutton_2['borderwidth'] = 3
            self.Overscan_Checkbutton_2['foreground'] = '#FF9999'
            self.Overscan_Checkbutton_2['relief'] = 'flat'

    def Window_Heater_Checkbutton_State_1(self):
        print('width Overscan_Checkbutton_1', self.Overscan_Checkbutton_1.winfo_width())
        print('height Overscan_Checkbutton_1', self.Overscan_Checkbutton_1.winfo_height())
        print('width Window_Heater_Checkbutton_1', self.Window_Heater_Checkbutton_1.winfo_width())
        print('height Window_Heater_Checkbutton_1', self.Window_Heater_Checkbutton_1.winfo_height())
        if self.window_heater_1 == 0:
            self.window_heater_1 = 1
        elif self.window_heater_1 == 1:
            self.window_heater_1 = 0
        else:
            pass
        return self.window_heater_1    
        
    def Window_Heater_Checkbutton_State_2(self):
        current_state = self.user_window_heater_2.get()
        if current_state == 1:
            self.Window_Heater_Checkbutton_2['text'] = "On"
            self.Window_Heater_Checkbutton_2['borderwidth'] = 3
            self.Window_Heater_Checkbutton_2['foreground'] = '#FF3864'
            self.Window_Heater_Checkbutton_2['relief'] = 'sunken'
        else:
            self.Window_Heater_Checkbutton_2['text'] = "Off"
            self.Window_Heater_Checkbutton_2['borderwidth'] = 3
            self.Window_Heater_Checkbutton_2['foreground'] = '#FF9999'
            self.Window_Heater_Checkbutton_2['relief'] = 'flat'


    def Epoch_Checkbutton_State_2000(self):
        self.epoch = "J2000"
        self.Epoch_2000.grid_forget()
        self.Epoch_Today.grid_forget()
        self.Epoch_2000 = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_2000,
                                                            colors=self.Common_Colors, status = "on", text="J2000")
        self.Epoch_2000.grid(row=5, column=1, padx=(5,5), pady=(10,5), sticky=E+W)        
        self.Epoch_Today = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_Today,
                                                        colors=self.Common_Colors, status = "off", text="Today")
        self.Epoch_Today.grid(row=5, column=2, padx=(5,5), pady=(10,5), sticky=E+W)
        return self.epoch

    def Epoch_Checkbutton_State_Today(self):
        self.epoch = "Today"
        self.Epoch_2000.grid_forget()
        self.Epoch_Today.grid_forget()
        self.Epoch_2000 = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_2000,
                                                            colors=self.Common_Colors, status = "off", text="J2000")
        self.Epoch_2000.grid(row=5, column=1, padx=(5,5), pady=(10,5), sticky=E+W)        
        self.Epoch_Today = CustomRadiobutton(self.Object_Frame, width=212, height=25, callback = self.Epoch_Checkbutton_State_Today,
                                                        colors=self.Common_Colors, status = "on", text="Today")
        self.Epoch_Today.grid(row=5, column=2, padx=(5,5), pady=(10,5), sticky=E+W)
        return self.epoch 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Camera Loop  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #       
    def _camera_talker(self):
            try:
                if self.Camera_Queue_Out.qsize() > 0:                        
                    query_result = self.Camera_Queue_Out.get()                        
                    if query_result[0] == "INIT":
                        number_of_cameras, serial_nums = self._init_cameras(query_result)
                        if number_of_cameras > 0:
                            for i in range(0,number_of_cameras):
                                quer_cmd = serial_nums[i] + '~' + 'QUER~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO'
                                self.Camera_Queue_In.put(['QUER', quer_cmd])
                            self._birger_init(self.serial_nums)
                    elif query_result[0] == "QUERY":
                        serial_number = query_result[1]
                        CCD_temp = query_result[2]
                        cooler_power = query_result[3]
                        heat_sink_temp = query_result[4]
                        main_sensor_state = query_result[5]
                        if serial_number == "AL3200M-18070201":
                            camera_name = "Harlequin"
                            self.Label_DefaultCCDTemp_1['text'] = str(CCD_temp)
                            self.Label_Cooler_Power_1['text'] = str(cooler_power)
                            self.Label_HeatSink_1['text'] = str(heat_sink_temp)
                            self.Vertical_Harlequin_Label['text'] = 'Harelquin Status:' + str(main_sensor_state)
                            if main_sensor_state == "8":
                                readout_command = self._readout_1(self)
                                self.Camera_Queue_In.put(['READOUT', readout_command])
                        elif serial_number == "AL3200M-18070401":
                            self.Label_DefaultCCDTemp_2['text'] = str(CCD_temp)
                            self.Label_Cooler_Power_2['text'] = str(cooler_power)
                            self.Label_HeatSink_2['text'] = str(heat_sink_temp)
                            self.Vertical_Bobwhite_Label['text'] = 'Bobwhite Status:' + str(main_sensor_state)
                            if main_sensor_state == "8":
                                readout_command = self._readout_2(self)
                                self.Camera_Queue_In.put(['READOUT', readout_command])                                    
                        else:
                            pass
                    else:
                        pass
                    if self.Command_Queue.qsize() > 0:
                        command = self.Command_Queue.get()
                        if ("QUIT" in command):
                            self._quit_GUI()                                
                        if ("AL3200M-18070201" in command):
                            harlequin_sensor_state = self.Vertical_Harlequin_Label['text']
                            if ("0" in harlequin_sensor_state):
                                if ("COOL" in command):
                                    self.Camera_Queue_In.put(['COOL', command])
                                elif ("EXPS" in command):
                                    self.Camera_Queue_In.put(['EXPOSE', command])
                                else:
                                    pass
                            else:
                                if ("ABRT" in command):
                                    self.Camera_Queue_In.put(['ABORT', command])
                                elif ("RDOT" in command):
                                    self.Camera_Queue_In.put(['READOUT', command])
                                    series = str(self.user_series_1.get())
                                    if series == "" or not series.isnumeric():
                                        self.Harlequin_Widget_Flash(5, self.Entry_UserTakeSeries_1)
                                    else:
                                        series = int(series) - 1
                                        self.user_series_1.set(series)
                                        if series > 0:
                                            self._take_exposure_1()
                                else:
                                    pass
                        if ("AL3200M-18070401" in command):
                            bobwhite_sensor_state = self.Vertical_Bobwhite_Label['text']
                            if ("0" in bobwhite_sensor_state):
                                if ("COOL" in command):
                                    self.Camera_Queue_In.put(['COOL', command])
                                elif ("EXPS" in command):
                                    self.Camera_Queue_In.put(['EXPOSE', command])
                                else:
                                    pass
                            else:
                                if ("ABRT" in command):
                                    self.Camera_Queue_In.put(['ABORT', command])
                                elif ("RDOT" in command):
                                    self.Camera_Queue_In.put(['READOUT', command])
                                    series = str(self.user_series_2.get())
                                    if series == "" or not series.isnumeric():
                                        self.Bobwhite_Widget_Flash(5, self.Entry_UserTakeSeries_2)
                                    else:
                                        series = int(series) - 1
                                        self.user_series_2.set(series)
                                        if series > 0:
                                            self._take_exposure_2()
                                else:
                                    pass                         
            except:
                pass            
            self.master.after(500, self._camera_talker)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COOLING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def _cool_CCD_1(self):
        # setpoint
        self.setpoint_1 = self.user_set_point_1.get()
        if self.setpoint_1 == "" or not self.setpoint_1.isnumeric():
            self.Harlequin_Widget_Flash(5, self.Entry_UserSetPoint_1)
        else:
            self.cooling_enabled_1 = 1              
            CCD_Temp_1 = self.Label_DefaultCCDTemp_1['text']       
            if CCD_Temp_1!='--':
                if round(int(float(CCD_Temp_1)) - int(float(self.setpoint_1)))!=0:
                    if abs(int(self.setpoint_1)) <= 9:
                        if int(self.setpoint_1) < 0:
                            cool_command = self.serial_number_1 + '~COOL' + '~1' + '~-' + '~0' + str(abs(int(self.setpoint_1))) + '~'
                        if int(self.setpoint_1) >= 0:
                            cool_command = self.serial_number_1 + '~COOL' + '~1' + '~+' + '~0' + str(abs(int(self.setpoint_1))) + '~'
                    if abs(int(self.setpoint_1)) >= 10:
                        if int(self.setpoint_1) < 0:
                            cool_command = self.serial_number_1 + '~COOL' + '~1' + '~-~' + str(abs(int(self.setpoint_1))) + '~'
                        if int(self.setpoint_1) >= 0:
                            cool_command = self.serial_number_1 + '~COOL' + '~1' + '~+~' + str(abs(int(self.setpoint_1))) + '~'
                    self.Command_Queue.put(cool_command)
                    self.Vertical_Harlequin_Label['text'] = "Harlequin Status: CCD Cooling"
                    self.Label_DefaultCoolingEnabled_1['text'] = "Enabled"
                if round(int(float(CCD_Temp_1)) - int(float(self.setpoint_1)))==0:
                    self.Vertical_Harlequin_Label['text'] =  "Harlequin Status: Ready"
            if CCD_Temp_1=='--':
                self.Vertical_Harlequin_Label['text'] =  "Harlequin Status: Disconnected" 
        return self.setpoint_1, self.cooling_enabled_1

    def _cool_CCD_2(self):
        # setpoint
        self.setpoint_2 = self.user_set_point_2.get()
        if self.setpoint_2 == "" or not self.setpoint_2.isnumeric():
            self.Bobwhite_Widget_Flash(5, self.Entry_UserSetPoint_2)
        else:
            self.cooling_enabled_2 = 1              
            CCD_Temp_2 = self.Label_DefaultCCDTemp_2['text']       
            if CCD_Temp_2!='--':
                if round(int(float(CCD_Temp_2)) - int(float(self.setpoint_2)))!=0:
                    if abs(int(self.setpoint_2)) <= 9:
                        if int(self.setpoint_2) < 0:
                            cool_command = self.serial_number_2  + '~COOL' + '~1' + '~-' + '~0' + str(abs(int(self.setpoint_2))) + '~'
                        if int(self.setpoint_2) >= 0:
                            cool_command = self.serial_number_2 + '~COOL' + '~1' + '~+' + '~0' + str(abs(int(self.setpoint_2))) + '~'
                    if abs(int(self.setpoint_2)) >= 10:
                        if int(self.setpoint_2) < 0:
                            cool_command = self.serial_number_2 + '~COOL' + '~1' + '~-~' + str(abs(int(self.setpoint_2))) + '~'
                        if int(self.setpoint_2) >= 0:
                            cool_command = self.serial_number_2 + '~COOL' + '~1' + '~+~' + str(abs(int(self.setpoint_2))) + '~'                    
                    self.Command_Queue.put(cool_command)
                    self.Vertical_Bobwhite_Label['text'] = "Bobwhite Status: CCD Cooling"
                    self.Label_DefaultCoolingEnabled_2['text'] = "Enabled"
                if round(int(float(CCD_Temp_2)) - int(float(self.setpoint_2)))==0:
                    self.Vertical_Bobwhite_Label['text'] =  "Bobwhite Status: Ready"
            if CCD_Temp_2=='--':
                self.Vertical_Bobwhite_Label['text'] =   "Bobwhite Status: Disconnected"
        return self.setpoint_2, self.cooling_enabled_2

    def _cool_all(self):
        # Camera 1
        self._cool_CCD_1(self)
        self._cool_CCD_2(self) 
        
    def _stop_cooling_1(self):
        self.cooling_enabled_1 = 0
        cool_command = self.serial_number_1 + '~COOL' + '~0' + '~+' + '~01~'
        self.Command_Queue.put(cool_command)
        self.Label_DefaultCoolingEnabled_1['text'] = "Disabled"
        return self.cooling_enabled_1

    def _stop_cooling_2(self):
        self.cooling_enabled_2 = 0
        cool_command = self.serial_number_2 + '~COOL' + '~0' + '~+' + '~01~'
        self.Command_Queue.put(cool_command)
        self.Label_DefaultCoolingEnabled_2['text'] = "Disabled"
        return self.cooling_enabled_2

    def _stop_cooling_all(self):
        self._stop_cooling_1()
        self._stop_cooling_2()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXPOSURE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def _take_exposure_1(self):
        # Exposure time
        exposure_time_1 = str(self.user_exposure_time_1.get())
        # Series
        series = str(self.user_series_1.get())
        # Preflash
        rbipreflashduration = str(self.user_preflash_duration_1.get())
        rbiflushes = str(self.user_preflash_clearout_1.get())
        isdigit_exptime_1 = exposure_time_1.replace(".",'',1)
        if exposure_time_1 == "" or not isdigit_exptime_1.isnumeric():
            self.Harlequin_Widget_Flash(5, self.Entry_UserExposureTime_1)
        elif series == "" or not series.isnumeric():
            self.Harlequin_Widget_Flash(5, self.Entry_UserTakeSeries_1)
        elif rbipreflashduration == "" or not rbipreflashduration.isnumeric():
            self.Harlequin_Widget_Flash(5, self.Entry_RBI_preflash_duration_1)
        elif rbiflushes == "" or not rbiflushes.isnumeric():
            self.Harlequin_Widget_Flash(5, self.Entry_RBI_Flushes_1)
        else:
            self.exposure_time_1 = float(exposure_time_1)
            self.series_1 = int(series)
            self.rbipreflashduration_1 = float(rbipreflashduration)
            self.rbiflushes_1 = int(rbiflushes)
            # Turn them into strings
            exposure = str(self.exposure_time_1)
            str_rbi = str(rbipreflashduration)
            str_flush = str(int(rbiflushes))            
            camera_name = "Harlequin"
            # Binning
            self.serial_number_1  = "AL3200M-18070201"
            s = self.user_binning_1.get()
            self.xbin_1 = s[0]
            self.ybin_1 = s[2]
            if s=="1x1":
                self.binning_1 = 0                
            elif s=="2x2":
                self.binning_1 = 1
            elif s=="3x3":
                self.binning_1 = 2            
            # shutter open/closed & frame type
            s = str(self.user_shutter_1.get())
            if s=="Light":
                self.shutter_1 = 1
                self.lightframe_1 = 0
                self.eolightframe = 1
                self.frametype_1 = "Light"
            elif s=="Dark":
                self.shutter_1 = 0
                self.lightframe_1 = 1
                self.eolightframe = 0
                self.frametype_1 = "Dark"
            elif s=="Bias":
                self.shutter_1 = 0
                self.lightframe_1 = 2
                self.eolightframe_1 = 0
                self.exposure_time_1 = 0.12
                self.frametype_1 = "Bias"
            elif s=="Flat":
                self.shutter_1 = 1
                self.lightframe_1 = 3
                self.eolightframe = 1
                self.frametype_1 = "Flat"
            # readout
            s = self.user_readout_1.get()
            if s=="1x1":
                self.readout_1 = 0
            elif s=="2x2":
                self.readout_1 = 1
            # overscan
            self.overscan_1 = str(self.user_overscan_1.get())
            # Exposure Command            
            command_exposure = self.serial_number_1 + "~EXPS~" + self.xbin_1 + "~" + self.ybin_1 + "~0~" + "0~" + exposure + '~' + str(self.shutter_1) + '~'            
            command_exposure = command_exposure + str(self.readout_1) + '~' + self.overscan_1 + '~' + str_rbi +'~' + str_flush + "~"
            self.Command_Queue.put(command_exposure)
            # Filter type
            self.filter_1 = self.user_filter_1.get()
            # Object Type
            try:
                object_name = self.user_object_name.get()
            except:
                object_name = "OBJECT"
            # RA Coordinates
            try:
                if self.Precessed_RA.text == "--":
                    ra = [self.RA_H.get(), self.RA_M.get(), self.RA_S.get()]
                else:
                    string_ra, string_dec, precessed_ra, precessed_dec = self.precess()
                    ra = precessed_ra
            except:
                ra = [0,0,0]
            # RA Coordinates
            try:
                if self.PRecessed_DEC.text == "--":
                    dec = [self.DEC_D.get(), self.DEC_M.get(), self.DEC_S.get()]
                else:
                    string_ra, string_dec, precessed_ra, precessed_dec = self.precess()
                    dec = precessed_dec
            except:
                dec = [0,0,0]
            # RA & DEC
            RA = str(ra[0]) + "h:" + str(ra[1]) + "m:" + str(ra[2]) + "s"
            DEC = str(dec[0]) + "h:" + str(dec[1]) + "m:" + str(dec[2]) + "s"
            # LMST
            LMST_RAW = Calculated_Values.calculateLMST()
            LMST = str(LMST_RAW[0]) + "h:" + str(LMST_RAW[1]) + "m:" + str(LMST_RAW[2]) + "s"
            # HA
            HA_RAW = Calculated_Values.calculateHourAngle(ra, LMST_RAW)
            HA = str(HA_RAW[0]) + "h:" + str(HA_RAW[1]) + "m:" + str(HA_RAW[2]) + "s"
            # Ambient Temperature
            tempC = self.sensor_push_api()
            # Birger Setting
            birger = str(self.birger_setpoint_1)
            # CCD Setpoint
            ccd_setpoint = self.user_set_point_1.get()
            # CCD Temperature
            ccd_temperature = self.Label_DefaultCCDTemp_1['text']
            # Folder        
            mydate = datetime.now()
            pathname = "/Users/observer/Desktop/PythonCode/images/" + str(mydate.year) + '-'+ str(mydate.month) +'-'
            pathname = pathname + str(mydate.day) + '+' + str(mydate.day+1) +  "/"
            if not path.exists(pathname):
                os.mkdir(pathname)
            filename = pathname + str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_1) + '.fits'
            if path.exists(filename):
                onlyfiles = [f for f in listdir(pathname) if isfile(join(pathname, f))]
                core_filename = str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_1)
                matches = [match for match in onlyfiles if core_filename in match]
                filenum = len(matches)-1
                filename = pathname + str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_1) + "_" + str(filenum) + '.fits'
            self.readout_command_1 = self.serial_number_1 + "~RDOT~" + self.overscan_1 + "~" + self.frametype_1 +"~"
            self.readout_command_1 = self.readout_command_1 + camera_name +"~" +exposure + "s~None~"
            self.readout_command_1 = self.readout_command_1 + LMST + "~" + RA + "~" + DEC + "~" + HA + "~" + str(tempC) + "~"
            self.readout_command_1 = self.readout_command_1 + birger + "~" + filename + "~"
            print(self.readout_command_1)
        return self.readout_command_1

    def _take_exposure_2(self):
        # exposure time
        exposure_time_2 = str(self.user_exposure_time_2.get())
        # Series
        series = str(self.user_series_2.get())
        # Preflash
        rbipreflashduration = str(self.user_preflash_duration_2.get())
        rbiflushes = str(self.user_preflash_clearout_2.get())
        isdigit_exptime_2 = exposure_time_2.replace(".",'',1)
        if exposure_time_2 == "" or not isdigit_exptime_2.isnumeric():
            self.Bobwhite_Widget_Flash(5, self.Entry_UserExposureTime_2)
        elif series == "" or not series.isnumeric():
            self.Bobwhite_Widget_Flash(5, self.Entry_UserTakeSeries_2)
        elif rbipreflashduration == "" or not rbipreflashduration.isnumeric():
            self.Bobwhite_Widget_Flash(5, self.Entry_RBI_preflash_duration_2)
        elif rbiflushes == "" or not rbiflushes.isnumeric():
            self.Bobwhite_Widget_Flash(5, self.Entry_RBI_Flushes_2)
        else:
            self.exposure_time_2 = float(exposure_time_2)
            self.series_2 = int(series)
            self.rbipreflashduration_2 = float(rbipreflashduration)
            self.rbiflushes_2 = int(rbiflushes)
            # Turn them into strings
            exposure = str(self.exposure_time_2)
            str_rbi = str(rbipreflashduration)
            str_flush = str(int(rbiflushes))            
            camera_name = "Bobwhite"
            # binning
            self.serial_number_2  = "AL3200M-18070401"
            s = self.user_binning_2.get()
            self.xbin_2 = s[0]
            self.ybin_2 = s[2]
            if s=="1x1":
                self.binning_2 = 0                
            elif s=="2x2":
                self.binning_2 = 1
            elif s=="3x3":
                self.binning_2 = 2            
            # shutter open/closed & frame type
            s = str(self.user_shutter_2.get())
            if s=="Light":
                self.shutter_2 = 1
                self.lightframe_2 = 0
                self.eolightframe = 1
                self.frametype_2 = "Light"
            elif s=="Dark":
                self.shutter_2 = 0
                self.lightframe_2 = 1
                self.eolightframe = 0
                self.frametype_2 = "Dark"
            elif s=="Bias":
                self.shutter_2 = 0
                self.lightframe_2 = 2
                self.eolightframe_2 = 0
                self.exposure_time_2 = 0.12
                self.frametype_2 = "Bias"
            elif s=="Flat":
                self.shutter_2 = 1
                self.lightframe_2 = 3
                self.eolightframe = 1
                self.frametype_2 = "Flat"
            # readout
            s = self.user_readout_2.get()
            if s=="1x1":
                self.readout_2 = 0
            elif s=="2x2":
                self.readout_2 = 1
            # overscan
            self.overscan_2 = str(self.user_overscan_2.get())
            # Exposure Command            
            command_exposure = self.serial_number_2 + "~EXPS~" + self.xbin_2 + "~" + self.ybin_2 + "~0~" + "0~" + exposure + '~' + str(self.shutter_2) + '~'            
            command_exposure = command_exposure + str(self.readout_2) + '~' + self.overscan_2 + '~' + str_rbi +'~' + str_flush + "~"
            self.Command_Queue.put(command_exposure)
            # Filter type
            self.filter_2 = self.user_filter_2.get()
            # Object Type
            try:
                object_name = self.user_object_name.get()
            except:
                object_name = "OBJECT"
            # RA Coordinates
            try:
                if self.Precessed_RA.text == "--":
                    ra = [self.RA_H.get(), self.RA_M.get(), self.RA_S.get()]
                else:
                    string_ra, string_dec, precessed_ra, precessed_dec = self.precess()
                    ra = precessed_ra
            except:
                ra = [0,0,0]
            # RA Coordinates
            try:
                if self.PRecessed_DEC.text == "--":
                    dec = [self.DEC_D.get(), self.DEC_M.get(), self.DEC_S.get()]
                else:
                    string_ra, string_dec, precessed_ra, precessed_dec = self.precess()
                    dec = precessed_dec
            except:
                dec = [0,0,0]
            # RA & DEC
            RA = str(ra[0]) + "h:" + str(ra[1]) + "m:" + str(ra[2]) + "s"
            DEC = str(dec[0]) + "h:" + str(dec[1]) + "m:" + str(dec[2]) + "s"
            # LMST
            LMST_RAW = Calculated_Values.calculateLMST()
            LMST = str(LMST_RAW[0]) + "h:" + str(LMST_RAW[1]) + "m:" + str(LMST_RAW[2]) + "s"
            # HA
            HA_RAW = Calculated_Values.calculateHourAngle(ra, LMST_RAW)
            HA = str(HA_RAW[0]) + "h:" + str(HA_RAW[1]) + "m:" + str(HA_RAW[2]) + "s"
            # Ambient Temperature
            tempC = self.sensor_push_api()
            # Birger Setting
            birger = str(self.birger_setpoint_2)
            # CCD Setpoint
            ccd_setpoint = self.user_set_point_2.get()
            # CCD Temperature
            ccd_temperature = self.Label_DefaultCCDTemp_2['text']
            # Folder        
            mydate = datetime.now()
            pathname = "/Users/observer/Desktop/PythonCode/images/" + str(mydate.year) + '-'+ str(mydate.month) +'-'
            pathname = pathname + str(mydate.day) + '+' + str(mydate.day+1) +  "/"
            if not path.exists(pathname):
                os.mkdir(pathname)
            filename = pathname + str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_2) + '.fits'
            if path.exists(filename):
                onlyfiles = [f for f in listdir(pathname) if isfile(join(pathname, f))]
                core_filename = str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_2)
                matches = [match for match in onlyfiles if core_filename in match]
                filenum = len(matches)-1
                filename = pathname + str(camera_name) + '_' + exposure + 's_None_' + str(self.frametype_2) + "_" + str(filenum) + '.fits'
            self.readout_command_2 = self.serial_number_2 + "~RDOT~" + self.overscan_2 + "~" + self.frametype_2 +"~"
            self.readout_command_2 = self.readout_command_2 + camera_name +"~" +exposure + "s~None~"
            self.readout_command_2 = self.readout_command_2 + LMST + "~" + RA + "~" + DEC + "~" + HA + "~" + str(tempC) + "~"
            self.readout_command_2 = self.readout_command_2 + birger + "~" + filename + "~"
        return self.readout_command_2


    def _expose_all(self):
        self._take_exposure_1()
        self._take_exposure_2()

    def _readout_1(self):
        self.Command_Queue.put(self.readout_command_1)

    def _readout_2(self):
        self.Command_Queue.put(self.readout_command_2)        

    def _abort_exposure_1(self):
        command_abort = self.serial_number_1 + "~ABRT~"
        self.Command_Queue.put(command_abort)

    def _abort_exposure_2(self):
        command_abort = self.serial_number_2 + "~ABRT~"
        self.Command_Queue.put(command_abort)

    def _abort_all(self):
        self._abort_exposure_1()
        self._abort_exposure_2()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SensorPush ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def sensor_push_api(self):
        # log in
        url = "https://api.sensorpush.com/api/v1/oauth/authorize"
        urlkeys = {'email': "quail@yorku.ca", 'password': 'weathernow'}
        urlheaders = {"accept": "application/json", "Content-Type":"application/json"}
        r = requests.post(url, json=urlkeys)
        response = r.text
        response = response.strip("{")
        response = response.strip("}")
        response = response.split(":")
        authorization_key = response[1].split(",")
        authorization_key = authorization_key[0]
        authorization_key = authorization_key[1:(len(authorization_key)-1)]
        # get access token
        url1 = "https://api.sensorpush.com/api/v1/oauth/accesstoken"
        urlkeys1 = {'authorization': authorization_key}
        r1 = requests.post(url1, json=urlkeys1)
        response1 = r1.text
        response1 = response1.strip("{")
        response1 = response1.strip("}")
        response1 = response1.split(":")
        access_token = response1[1]
        access_token = access_token[1:(len(access_token)-1)]
        # get temperature
        url2 = "https://api.sensorpush.com/api/v1/samples"
        urlkeys2 =  {'accesstoken': access_token}
        urlkeys3 = {"limit":1}
        at = 'TOK:<' + access_token + '>'
        r2 = requests.post(url2,  headers={'accept':'application/json',
                       'Authorization': '{}'.format(access_token)}, json=urlkeys3)
        response2 = r2.text
        response2 = response2.split(",")
        temp_array = [match for match in response2 if "temperature" in match]
        temp_array = temp_array[0]
        temp_array = temp_array.split(":")
        temp = float(temp_array[1])
        tempC = (temp-32)/1.8
        tempC = (int(tempC*100))/100
        return tempC 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Birger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #     
    def _birger_init(self, serial_nums):
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.getoutput(["ls /dev/tty.*"])
        df = df.split("/dev/tty.")
        ports = []
        self.serial_nums = serial_nums
        for i in range(0, len(df)):
            d = df[i]
            if "usbserial" in d:
                d = d.strip("\n")
                ports.append(d)
        if len(ports) == 0:
            self.port_1 = None
            self.port_2 = None
        if len(ports) == 1:
            self.port_1 = "/Users/observer/Desktop/QUAIL_Soft/Birger/birger_exec -p /dev/cu." + ports[0]
            init_command = self.port_1 + " init"
            self.port_2 = None
            self.poutput_init_1 = subprocess.getoutput(init_command)            
            if not ("Error" in self.poutput_init_1):
                self._birger_status_1()
        if len(ports) == 2:
            port_1 = "/Users/observer/Desktop/QUAIL_Soft/Birger/birger_exec -p /dev/cu." + ports[0]
            init_command = port_1 + " init"
            poutput_init_1 = subprocess.getoutput(init_command)
            if not ("Error" in poutput_init_1):
                if 'FT2HLANS' in port_1:
                    bobwhite_location = self.serial_nums.index('AL3200M-18070401')
                    if bobwhite_location == 0:
                        self.port_1 = port_1
                    elif bobwhite_location == 1:
                        self.port_2 = port_1
                if 'FT2HLEDR' in port_1:
                    harlequin_location = self.serial_nums.index('AL3200M-18070201')
                    if harlequin_location == 0:
                        self.port_1 = port_1
                    elif harlequin_location == 1:
                        self.port_2 = port_1
            port_2 = "/Users/observer/Desktop/QUAIL_Soft/Birger/birger_exec -p /dev/cu." + ports[1]
            init_command = port_1 + " init"
            poutput_init_2 = subprocess.getoutput(init_command)            
            if not ("Error" in poutput_init_2):
                if 'FT2HLEDR' in port_2:
                    harlequin_location = self.serial_nums.index('AL3200M-18070201')
                    if harlequin_location == 0:
                        self.port_1 = port_2
                    elif harlequin_location == 1:
                        self.port_2 = port_2
                if 'FT2HLANS' in port_2:
                    bobwhite_location = self.serial_nums.index('AL3200M-18070401')
                    if bobwhite_location == 0:
                        self.port_1 = port_2
                    elif bobwhite_location == 1:
                        self.port_2 = port_2
            self._birger_status_1()
            self._birger_status_2()
        return self.port_1, self.port_2

    def _birger_status_1(self):
        command =  self.port_1 + " status"
        poutput_status = subprocess.getoutput(command)
        poutput_status = str(poutput_status)
        poutput_status = poutput_status.split("\n")
        self.birger_values_1 = []
        for i in range(0, len(poutput_status)):
            a = poutput_status[i].split(':')
            if len(a)>1:
                self.birger_values_1.append(a[1])
        self.birger_setpoint_1 = self.birger_values_1[0]
        self.max_birger_setpoint_1 = self.birger_values_1[2]
        self.Birger_Scrollbar_1.set(self.birger_setpoint_1)
        self.Birger_Scrollbar_1["to"] = self.max_birger_setpoint_1
        return self.birger_setpoint_1, self.max_birger_setpoint_1        

    def _birger_status_2(self):
        command =  self.port_2 + " status"
        poutput_status = subprocess.getoutput(command)
        poutput_status = str(poutput_status)
        poutput_status = poutput_status.split("\n")
        self.birger_values_2 = []
        for i in range(0, len(poutput_status)):
            a = poutput_status[i].split(':')
            if len(a)>1:
                self.birger_values_2.append(a[1])
        self.birger_setpoint_2 = self.birger_values_2[0]
        self.max_birger_setpoint_2 = self.birger_values_2[2]
        self.Birger_Scrollbar_2.set(self.birger_setpoint_2)
        self.Birger_Scrollbar_2["to"] = self.max_birger_setpoint_2
        return self.birger_setpoint_2, self.max_birger_setpoint_2

    def _birger_goto_1(self):
        birger_setpoint_1 = self.birger_entry_setpoint_1.get()        
        if birger_setpoint_1 == "":
            self.birger_setpoint_1 = self.birger_scale_setpoint_1.get()
        else:
            if not birger_setpoint_1.isnumeric():
                self.Harlequin_Widget_Flash(5, self.Entry_GoTo_1)
            else:
                self.birger_setpoint_1 = int(self.birger_entry_setpoint_1.get())
                self.Birger_Scrollbar_1.set(int(self.birger_setpoint_1)) 
        try:
            command = self.port_1 + " goto " + str(self.birger_setpoint_1)
            self.poutput_goto = subprocess.getoutput(command)
            self._birger_status_1()
            self._birger_status_2()
        except:
            pass        
        return self.birger_setpoint_1

    def _birger_goto_2(self):
        birger_setpoint_2 = self.birger_entry_setpoint_2.get()        
        if birger_setpoint_2 == "":
            self.birger_setpoint_2 = self.birger_scale_setpoint_2.get()
        else:
            if not birger_setpoint_2.isnumeric():
                self.Bobwhite_Widget_Flash(5, self.Entry_GoTo_2)
            else:
                self.birger_setpoint_2 = int(self.birger_entry_setpoint_2.get())
                self.Birger_Scrollbar_2.set(int(self.birger_setpoint_2))  
        try:
            command = self.port_2 + " goto " + str(self.birger_setpoint_2)
            self.poutput_goto = subprocess.getoutput(command)
            self._birger_status_2()
            self._birger_status_1()
        except:
            pass        
        return self.birger_setpoint_2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Ginga ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def cursor_cb_1(self, viewer, button, data_x, data_y):
        try:
            value = viewer.get_data(int(data_x + viewer.data_off),int(data_y + viewer.data_off))           
        except Exception:
            value = None
        fits_x, fits_y = data_x + 1, data_y + 1
        try:
            image = viewer.get_image()
            if image is None:
                return
            ra_txt, dec_txt = image.pixtoradec(fits_x, fits_y, format='str', coords='fit')
        except Exception as e:
            ra_txt = str(int(fits_x))
            dec_txt = str(int(fits_y))
        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (ra_txt, dec_txt, fits_x, fits_y, value)
        X_Text = ra_txt
        Y_Text = dec_txt
        Value_Text = str(value)
        self.X_Pixel_1.config(text=X_Text)
        self.Y_Pixel_1.config(text=Y_Text)
        self.Value_Pixel_1.config(text=Value_Text)
        self.data_x_1 = data_x
        self.data_y_1 = data_y
        return self.data_x_1, self.data_y_1

    def cursor_cb_2(self, viewer, button, data_x, data_y):
        try:
            value = viewer.get_data(int(data_x + viewer.data_off),int(data_y + viewer.data_off))            
        except Exception:
            value = None
        fits_x, fits_y = data_x + 1, data_y + 1
        try:
            image = viewer.get_image()
            if image is None:
                return
            ra_txt, dec_txt = image.pixtoradec(fits_x, fits_y, format='str', coords='fits')
        except Exception as e:
            ra_txt = str(int(fits_x))
            dec_txt = str(int(fits_y))
        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (ra_txt, dec_txt, fits_x, fits_y, value)
        X_Text = ra_txt
        Y_Text = dec_txt
        Value_Text = str(value)
        self.X_Pixel_2.config(text=X_Text)
        self.Y_Pixel_2.config(text=Y_Text)
        self.Value_Pixel_2.config(text=Value_Text)
        self.data_x_2 = data_x
        self.data_y_2 = data_y
        return self.data_x_2, self.data_y_2
    
    def mouse_zoom_1(self, event):
        in_or_out = event.delta
        try:
            if self.data_x_1 != None and self.data_y_1 != None:
                viewer = self.fi_1
                viewer.set_pan(self.data_x_1, self.data_y_1)
        except:
            pass
        if in_or_out > 0:
            self.zoom_in_1()
        if in_or_out < 0:
            self.zoom_out_1()

    def mouse_zoom_2(self, event):
        in_or_out = event.delta
        try:
            if self.data_x_2 != None and self.data_y_2 != None:
                viewer = self.fi_1
                viewer.set_pan(self.data_x_2, self.data_y_2)
        except:
            pass
        if in_or_out > 0:
            self.zoom_in_2()
        if in_or_out < 0:
            self.zoom_out_2()

    def zoom_in_1(self, event=None):
        viewer = self.fi_1
        self.current_zoom_value_1 = viewer.get_zoom()
        self.current_zoom_value_1 = self.current_zoom_value_1 + 1/4
        viewer.zoom_to(self.current_zoom_value_1)
        return self.current_zoom_value_1

    def zoom_out_1(self, event=None):
        viewer = self.fi_1
        self.current_zoom_value_1 = viewer.get_zoom()
        self.current_zoom_value_1 = self.current_zoom_value_1 - 1/4
        viewer.zoom_to(self.current_zoom_value_1)        
        return self.current_zoom_value_1

    def zoom_fit_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = self.zoom_fit_value_1
        viewer.set_pan(self.pan_center_value_1[0], self.pan_center_value_1[1])
        viewer.zoom_to(self.zoom_fit_value_1)
        return self.current_zoom_value_1

    def zoom_to_quater_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = -4
        viewer.zoom_to(-4)
        return self.current_zoom_value_1

    def zoom_to_half_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = -2
        viewer.zoom_to(-2)
        return self.current_zoom_value_1

    def zoom_to_one_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = 1
        viewer.zoom_to(1)
        return self.current_zoom_value_1
    
    def zoom_to_two_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = 2
        viewer.zoom_to(2)
        return self.current_zoom_value_1

    def zoom_to_four_1(self):
        viewer = self.fi_1
        self.current_zoom_value_1 = 4
        viewer.zoom_to(4)
        return self.current_zoom_value_1    

    def zoom_in_2(self, event=None):
        viewer = self.fi_2
        self.current_zoom_value_2 = viewer.get_zoom()
        self.current_zoom_value_2 = self.current_zoom_value_2 + 1/4
        viewer.zoom_to(self.current_zoom_value_2)
        return self.current_zoom_value_2

    def zoom_out_2(self, event=None):
        viewer = self.fi_2
        self.current_zoom_value_2 = viewer.get_zoom()
        self.current_zoom_value_2 = self.current_zoom_value_2 - 1/4
        viewer.zoom_to(self.current_zoom_value_2)        
        return self.current_zoom_value_2

    def zoom_fit_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = self.zoom_fit_value_2
        viewer.set_pan(self.pan_center_value_2[0], self.pan_center_value_2[1])
        viewer.zoom_to(self.zoom_fit_value_2)
        return self.current_zoom_value_2

    def zoom_to_quater_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = -4
        viewer.zoom_to(-4)
        return self.current_zoom_value_2

    def zoom_to_half_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = -2
        viewer.zoom_to(-2)
        return self.current_zoom_value_2

    def zoom_to_one_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = 1
        viewer.zoom_to(1)
        return self.current_zoom_value_2
    
    def zoom_to_two_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = 2
        viewer.zoom_to(2)
        return self.current_zoom_value_2

    def zoom_to_four_2(self):
        viewer = self.fi_2
        self.current_zoom_value_2 = 4
        viewer.zoom_to(4)
        return self.current_zoom_value_2

    def set_scale_minmax_1(self):        
        self.scale_1 = "minmax"
        try:
            self.Scale_Linear_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_Log_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_MinMax_1.configure(style="HarlequinSunkenButton.TButton")
            self.Scale_ZScale_1.configure(style="HarlequinRaisedButton.TButton")
        except:
            pass 
        viewer = self.fi_1                
        viewer.set_autocut_params('minmax')
        return self.scale_1

    def set_scale_zscale_1(self):
        self.scale_1 = "zscale"
        try:
            self.Scale_Linear_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_Log_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_MinMax_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_ZScale_1.configure(style="HarlequinSunkenButton.TButton")
        except:
            pass        
        viewer = self.fi_1        
        viewer.set_autocut_params('zscale')
        return self.scale_1        

    def scale_linear_1(self):
        try:
            self.Scale_Linear_1.configure(style="HarlequinSunkenButton.TButton")
            self.Scale_Log_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_MinMax_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_ZScale_1.configure(style="HarlequinRaisedButton.TButton")
        except:
            pass
        self.scale_type_1 = "linear"
        viewer = self.fi_1
        viewer.set_color_algorithm('linear')        
        if self.scale_1 == "minmax":
            viewer.set_autocut_params('minmax')
            ac = Minmax(viewer.get_logger())
        if self.scale_1 == "zscale":                       
            viewer.set_autocut_params('zscale')            
            ac = ZScale(viewer.get_logger(), contrast=0.4)
        viewer.set_autocuts(ac)
        return self.scale_type_1
                       
    def scale_log_1(self):
        try:
            self.Scale_Linear_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_Log_1.configure(style="HarlequinSunkenButton.TButton")
            self.Scale_MinMax_1.configure(style="HarlequinRaisedButton.TButton")
            self.Scale_ZScale_1.configure(style="HarlequinRaisedButton.TButton")
        except:
            pass
        viewer = self.fi_1        
        self.scale_type_1 = "log"
        viewer.set_color_algorithm('log')
        if self.scale_1 == "minmax":
            viewer.set_autocut_params('minmax')
            ac = Minmax(viewer.get_logger())
        elif self.scale_1 == "zscale":
            viewer.set_autocut_params('zscale')  
            ac = ZScale(viewer.get_logger(), contrast=0.4)
        else:
            pass
        viewer.set_autocuts(ac)
        return self.scale_type_1           

    def set_scale_minmax_2(self):        
        self.scale_2 = "minmax"
        try:
            self.Scale_Linear_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_Log_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_MinMax_2.configure(style="BobwhiteSunkenButton.TButton")
            self.Scale_ZScale_2.configure(style="BobwhiteRaisedButton.TButton")
        except:
            pass 
        viewer = self.fi_2                
        viewer.set_autocut_params('minmax')
        return self.scale_2

    def set_scale_zscale_2(self):
        self.scale_2 = "zscale"
        try:
            self.Scale_Linear_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_Log_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_MinMax_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_ZScale_2.configure(style="BobwhiteSunkenButton.TButton")
        except:
            pass        
        viewer = self.fi_2        
        viewer.set_autocut_params('zscale')
        return self.scale_2        

    def scale_linear_2(self):
        try:
            self.Scale_Linear_2.configure(style="BobwhiteSunkenButton.TButton")
            self.Scale_Log_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_MinMax_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_ZScale_2.configure(style="BobwhiteRaisedButton.TButton")
        except:
            pass
        self.scale_type_2 = "linear"
        viewer = self.fi_2
        viewer.set_color_algorithm('linear')        
        if self.scale_2 == "minmax":
            viewer.set_autocut_params('minmax')
            ac = Minmax(viewer.get_logger())
        if self.scale_2 == "zscale":                       
            viewer.set_autocut_params('zscale')            
            ac = ZScale(viewer.get_logger(), contrast=0.4)
        viewer.set_autocuts(ac)
        return self.scale_type_2
                       
    def scale_log_2(self):
        try:
            self.Scale_Linear_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_Log_2.configure(style="BobwhiteSunkenButton.TButton")
            self.Scale_MinMax_2.configure(style="BobwhiteRaisedButton.TButton")
            self.Scale_ZScale_2.configure(style="BobwhiteRaisedButton.TButton")
        except:
            pass
        viewer = self.fi_2        
        self.scale_type_2 = "log"
        viewer.set_color_algorithm('log')
        if self.scale_2 == "minmax":
            viewer.set_autocut_params('minmax')
            ac = Minmax(viewer.get_logger())
        elif self.scale_2 == "zscale":
            viewer.set_autocut_params('zscale')  
            ac = ZScale(viewer.get_logger(), contrast=0.4)
        else:
            pass
        viewer.set_autocuts(ac)
        return self.scale_type_2
    
    def imexamine_a_1(self):
        self.Canvas_1.bind('a', self.aimexam_1)
        plots = Imexamine()
        plots.aper_phot_pars['radius'][0] = 15

    def imexamine_a_2(self):
        self.Canvas_2.bind('a', self.aimexam_2)
        plots = Imexamine()
        plots.aper_phot_pars['radius'][0] = 15

    def aimexam_1(self, event):
        result = plots.aper_phot(int(self.data_x_1),int(self.data_y_1), self.data_1, genplot=False, fig=None, error=None)
        x = result[4][0]
        y = result[4][1]
        flux = result[4][3]
        mag = result[4][4]
        sky = result[3]
        results = plots.line_fit(int(x), int(y), self.data_1, genplot=False)
        gaussfun = results[0]
        A = gaussfun.amplitude.value
        Mu = gaussfun.mean.value
        Sigma = gaussfun.stddev.value
        FWHM = 2*np.sqrt(2*np.log(2))*Sigma
        FWHM = int(FWHM*100)/100
        # Updating Labels
        # Star Data
        self.Star_Data_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="Star Data ", style="HarlequinThird.TLabel")
        self.Star_Data_Label_1.grid(row=11, column=2,columnspan=2, padx=(5,5), pady=(0,0), sticky=E+W)
        sep_info_3 = ttk.Separator(self.DS9_Info_Panel_1,orient=HORIZONTAL, style='Harlequin.TSeparator')
        sep_info_3.grid(row=12, column=2,columnspan=2, padx=(5,5), pady=(0,0), sticky=E+W)
        # XC
        self.XCentroid_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="XC: ", style="HarlequinSmall.TLabel")
        self.XCentroid_Label_1.grid(row=13, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.XCentroid_1 = ttk.Label(self.DS9_Info_Panel_1, text=str(x), style="HarlequinSmall.TLabel")
        self.XCentroid_1.grid(row=13, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        # YC
        self.YCentroid_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="YC: ", style="HarlequinSmall.TLabel")
        self.YCentroid_Label_1.grid(row=14, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.YCentroid_1 = ttk.Label(self.DS9_Info_Panel_1, text=str(y), style="HarlequinSmall.TLabel")
        self.YCentroid_1.grid(row=14, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        # FWHM
        self.FWHM_Label_1 = ttk.Label(self.DS9_Info_Panel_1, text="FWHM: ", style="HarlequinSmall.TLabel")
        self.FWHM_Label_1.grid(row=15, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.FWHM_1 = ttk.Label(self.DS9_Info_Panel_1, text=str(FWHM), style="HarlequinSmall.TLabel")
        self.FWHM_1.grid(row=15, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        
    def aimexam_2(self, event):
        #print(self.data_x, self.data_y)
        result = plots.aper_phot(int(self.data_x_2),int(self.data_y_2), self.data_2, genplot=False, fig=None, error=None)
        x = result[4][0]
        y = result[4][1]
        flux = result[4][3]
        mag = result[4][4]
        sky = result[3]
        results = plots.line_fit(int(x), int(y), self.data_2, genplot=False)
        gaussfun = results[0]
        A = gaussfun.amplitude.value
        Mu = gaussfun.mean.value
        Sigma = gaussfun.stddev.value
        FWHM = 2*np.sqrt(2*np.log(2))*Sigma
        FWHM = int(FWHM*100)/100
        # Updating Labels
        # Star Data
        self.Star_Data_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="Star Data ", style="BobwhiteThird.TLabel")
        self.Star_Data_Label_2.grid(row=11, column=2,columnspan=2, padx=(5,5), pady=(0,0), sticky=E+W)
        sep_info_3 = ttk.Separator(self.DS9_Info_Panel_2,orient=HORIZONTAL, style='Bobwhite.TSeparator')
        sep_info_3.grid(row=12, column=2,columnspan=2, padx=(5,5), pady=(0,0), sticky=E+W)
        # XC
        self.XCentroid_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="XC: ", style="BobwhiteSmall.TLabel")
        self.XCentroid_Label_2.grid(row=13, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.XCentroid_2 = ttk.Label(self.DS9_Info_Panel_2, text=str(x), style="BobwhiteSmall.TLabel")
        self.XCentroid_2.grid(row=13, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        # YC
        self.YCentroid_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="YC: ", style="BobwhiteSmall.TLabel")
        self.YCentroid_Label_2.grid(row=14, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.YCentroid_2 = ttk.Label(self.DS9_Info_Panel_2, text=str(y), style="BobwhiteSmall.TLabel")
        self.YCentroid_2.grid(row=14, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        # FWHM
        self.FWHM_Label_2 = ttk.Label(self.DS9_Info_Panel_2, text="FWHM: ", style="BobwhiteSmall.TLabel")
        self.FWHM_Label_2.grid(row=15, column=2,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
        self.FWHM_2 = ttk.Label(self.DS9_Info_Panel_2, text=str(FWHM), style="BobwhiteSmall.TLabel")
        self.FWHM_2.grid(row=15, column=3,columnspan=1, padx=(5,5), pady=(3,3), sticky=W)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Precess ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def precess(self):
        epoch = self.epoch
        RA_H = self.RA_H.get()
        RA_M = self.RA_M.get()
        RA_S = self.RA_S.get()
        DEC_D = self.DEC_D.get()
        DEC_M = self.DEC_M.get()
        DEC_S = self.DEC_S.get()
        if RA_H == "" or not RA_H.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_RA_H)
        if RA_M == "" or not RA_M.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_RA_M)
        if RA_S == "" or not RA_S.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_RA_S)
        if DEC_D == "" or not DEC_D.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_DEC_D)
        if DEC_M == "" or not DEC_M.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_DEC_M)
        if DEC_S == "" or not DEC_S.isnumeric():
            self.Common_Widget_Flash(5, self.Entry_DEC_S)
        string_ra = ""
        string_dec = ""
        precessed_ra = [0,0,0]
        precessed_dec = [0,0,0]
        try:             
            if epoch == "Today":
                Modern_RA, Modern_DEC, Modern_Epoch = Calculated_Values.epochConvert((int(RA_H),int(RA_M),int(RA_S)), (int(DEC_D),int(DEC_M),int(DEC_S)), 2012.5)
                self.Precessed_RA['text'] = str(Modern_RA[0]) + "h:" + str(Modern_RA[1]) + "m:" + str(int(Modern_RA[2]))+'s'
                string_ra = str(Modern_RA[0]) + "h:" + str(Modern_RA[1]) + "m:" + str(int(Modern_RA[2]))+'s'
                self.Precessed_DEC['text'] = str(Modern_DEC[0]) + "d:" + str(Modern_DEC[1]) + "m:" + str(int(Modern_DEC[2]))+'s'
                string_dec = str(Modern_DEC[0]) + "d:" + str(Modern_DEC[1]) + "m:" + str(int(Modern_DEC[2]))+'s'
                precessed_ra = [Modern_RA[0], Modern_RA[1], Modern_RA[2]]
                precessed_dec = [Modern_DEC[0], Modern_DEC[1], Modern_DEC[2]]
            elif epoch == "J2000":
                self.Precessed_RA['text'] = str(RA_H) + "h:" + str(RA_M) + "m:" + str(int(RA_S))+'s'
                string_ra = str(RA_H) + "h:" + str(RA_M) + "m:" + str(int(RA_S))+'s'
                self.Precessed_DEC['text'] = str(DEC_D) + "d:" + str(DEC_M) + "m:" + str(int(DEC_S))+'s'
                string_dec = str(DEC_D) + "d:" + str(DEC_M) + "m:" + str(int(DEC_S))+'s'
                precessed_ra = [int(RA_H), int(RA_M), int(RA_S)]
                precessed_dec = [int(DEC_D), int(DEC_M), int(DEC_S)]
            else:
                pass
        except:
            pass

        return string_ra, string_dec, precessed_ra, precessed_dec


    def Common_Widget_Flash(self, times, widget):
        if widget['style'] == "Common.TEntry":
            widget['style'] = "Error.TEntry"
        else:
            widget['style'] = "Common.TEntry"
        times = times - 1
        if times > 0:
            widget.after(100, lambda t=times: self.Common_Widget_Flash(t, widget))
        else:
            widget['style'] = "Common.TEntry"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DS9 Panel ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #     
    def reset_button_states_1(self):
        self.Scale_Button_1.grid_forget()
        self.Aperphot_Button_1.grid_forget()
        if self.pressed_zoom_count_1 == 1:
            self.Zoom_Button_In_1.grid_forget()
            self.Zoom_Button_Out_1.grid_forget()
            self.Zoom_Button_Fit_1.grid_forget()
            self.Zoom_Button_025_1.grid_forget()
            self.Zoom_Button_05_1.grid_forget()
            self.Zoom_Button_1_1.grid_forget()
            self.Zoom_Button_2_1.grid_forget()
            self.Zoom_Button_4_1.grid_forget()            
        if self.pressed_scale_count_1 == 1:            
            self.Scale_Linear_1.grid_forget()
            self.Scale_Log_1.grid_forget()
            self.Scale_MinMax_1.grid_forget()
            self.Scale_ZScale_1.grid_forget()
        if self.pressed_aperphot_count_1 == 1:
            self.Imexamine_A_1.grid_forget()
        return self.current_zoom_value_1, self.pressed_scale_count_1, self.pressed_aperphot_count_1

    def show_zoom_options_1(self):
        self.Zoom_Style_1 = self.Zoom_Button_1['style']
        if self.Zoom_Style_1 == "HarlequinRaisedButton.TButton":            
            self.Zoom_Button_1.configure(style="HarlequinSunkenButton.TButton")
            self.reset_button_states_1()
            self.Scale_Button_1.grid_forget()
            self.Aperphot_Button_1.grid_forget()
            # Zoom In
            self.Zoom_Button_In_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom In", style="HarlequinRaisedButton.TButton", width=8, command = self.zoom_in_1)
            self.Zoom_Button_In_1.grid(row=2, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)        
            # Zoom Out
            self.Zoom_Button_Out_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom Out",  style="HarlequinRaisedButton.TButton",width=8, command = self.zoom_out_1)
            self.Zoom_Button_Out_1.grid(row=3, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)         
            # Zoom Fit
            self.Zoom_Button_Fit_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom Fit", style="HarlequinRaisedButton.TButton",width=8, command = self.zoom_fit_1)
            self.Zoom_Button_Fit_1.grid(row=4, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)       
            # Zoom 1/4
            self.Zoom_Button_025_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom 1/4", style="HarlequinRaisedButton.TButton", width=8, command = self.zoom_to_quater_1)
            self.Zoom_Button_025_1.grid(row=5, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)         
            # Zoom 1/2
            self.Zoom_Button_05_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom 1/2", style="HarlequinRaisedButton.TButton",width=8, command = self.zoom_to_half_1)
            self.Zoom_Button_05_1.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E) 
            # Zoom 1
            self.Zoom_Button_1_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom 1", style="HarlequinRaisedButton.TButton",width=8, command = self.zoom_to_one_1)
            self.Zoom_Button_1_1.grid(row=7, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Zoom 2
            self.Zoom_Button_2_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom 2", style="HarlequinRaisedButton.TButton",width=8, command = self.zoom_to_two_1)
            self.Zoom_Button_2_1.grid(row=8, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E) 
            # Zoom 4
            self.Zoom_Button_4_1 = ttk.Button(self.DS9_Button_Frame_1, text="Zoom 4", style="HarlequinRaisedButton.TButton", width=8, command = self.zoom_to_four_1)
            self.Zoom_Button_4_1.grid(row=9, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", width=10, command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=10, column=1, columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
            # Aperphot
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",   style="HarlequinRaisedButton.TButton", width=10, command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=11, column=1, columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
            self.pressed_zoom_count_1 = 1
        if self.Zoom_Style_1 == "HarlequinSunkenButton.TButton":            
            self.Zoom_Button_1.configure(style="HarlequinRaisedButton.TButton")
            self.reset_button_states_1()
            # Scale
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", width=10, command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            # IRAF
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",  style="HarlequinRaisedButton.TButton",  width=10, command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_zoom_count_1 = 0            
        return self.current_zoom_value_1, self.pressed_scale_count_1, self.pressed_aperphot_count_1

    def show_scale_options_1(self):
        self.Zoom_Button_1.configure(style="HarlequinRaisedButton.TButton")
        self.Scale_Style_1 = self.Scale_Button_1['style']
        if self.Scale_Style_1 == "HarlequinRaisedButton.TButton":                   
            self.reset_button_states_1()
            # Scale
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinSunkenButton.TButton", command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            # Scale Linear
            self.Scale_Linear_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Linear ",  style = "HarlequinRaisedButton.TButton", width=8, command = self.scale_linear_1)
            self.Scale_Linear_1.grid(row=3, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale Log
            self.Scale_Log_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Log ",  style = "HarlequinRaisedButton.TButton",  width=8,command = self.scale_log_1)
            self.Scale_Log_1.grid(row=4, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale MinMax
            self.Scale_MinMax_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Min Max ",  style = "HarlequinRaisedButton.TButton", width=8, command = self.set_scale_minmax_1)
            self.Scale_MinMax_1.grid(row=5, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale ZScale
            self.Scale_ZScale_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Zscale ",  style = "HarlequinRaisedButton.TButton", width=8, command = self.set_scale_zscale_1)
            self.Scale_ZScale_1.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # IRAF
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",   style="HarlequinRaisedButton.TButton", command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=7, column=1, columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
            self.pressed_scale_count_1 = 1
        if self.Scale_Style_1 == "HarlequinSunkenButton.TButton":
            self.Scale_Button_1.configure(style="HarlequinRaisedButton.TButton")
            self.reset_button_states_1()
            # IRAF
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",  style="HarlequinRaisedButton.TButton", command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_scale_count_1 = 0
        return self.current_zoom_value_1, self.pressed_scale_count_1, self.pressed_aperphot_count_1

    def show_aperphot_options_1(self):
        self.Zoom_Button_1.configure(style="HarlequinRaisedButton.TButton")
        self.IRAF_Style_1 = self.Aperphot_Button_1['style']
        if self.IRAF_Style_1 == "HarlequinRaisedButton.TButton":          
            self.reset_button_states_1()
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",  style="HarlequinSunkenButton.TButton", command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            # Aperphot Imexamine a
            self.Imexamine_A_1 = ttk.Button(self.DS9_Button_Frame_1, text="AperPhot",  style = "HarlequinRaisedButton.TButton", width=8,  command = self.imexamine_a_1)
            self.Imexamine_A_1.grid(row=4, column=1, columnspan=1, rowspan=1, padx=(5,0), pady=(0,0), sticky=E)
            self.pressed_aperphot_count_1 = 1
        if self.IRAF_Style_1 == "HarlequinSunkenButton.TButton":
            self.Aperphot_Button_1.configure(style="HarlequinRaisedButton.TButton")
            self.reset_button_states_1()
            self.Scale_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" Scale ",   style="HarlequinRaisedButton.TButton", command = self.show_scale_options_1)
            self.Scale_Button_1.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_1 = ttk.Button(self.DS9_Button_Frame_1, text=" IRAF ",  style="HarlequinRaisedButton.TButton", command = self.show_aperphot_options_1)
            self.Aperphot_Button_1.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_aperphot_count_1 = 0
        return self.current_zoom_value_1, self.pressed_scale_count_1, self.pressed_aperphot_count_1

    def reset_button_states_2(self):
        self.Scale_Button_2.grid_forget()
        self.Aperphot_Button_2.grid_forget()
        if self.pressed_zoom_count_2 == 1:
            self.Zoom_Button_In_2.grid_forget()
            self.Zoom_Button_Out_2.grid_forget()
            self.Zoom_Button_Fit_2.grid_forget()
            self.Zoom_Button_025_2.grid_forget()
            self.Zoom_Button_05_2.grid_forget()
            self.Zoom_Button_1_2.grid_forget()
            self.Zoom_Button_2_2.grid_forget()
            self.Zoom_Button_4_2.grid_forget()            
        if self.pressed_scale_count_2 == 1:
            self.Scale_Linear_2.grid_forget()
            self.Scale_Log_2.grid_forget()
            self.Scale_MinMax_2.grid_forget()
            self.Scale_ZScale_2.grid_forget()
        if self.pressed_aperphot_count_2 == 1:
            self.Imexamine_A_2.grid_forget()
        return self.current_zoom_value_2, self.pressed_scale_count_2, self.pressed_aperphot_count_2

    def show_zoom_options_2(self):
        self.Zoom_Style_2 = self.Zoom_Button_2['style']
        if self.Zoom_Style_2 == "BobwhiteRaisedButton.TButton":            
            self.Zoom_Button_2.configure(style="BobwhiteSunkenButton.TButton")
            self.reset_button_states_2()
            self.Scale_Button_2.grid_forget()
            self.Aperphot_Button_2.grid_forget()
            # Zoom In
            self.Zoom_Button_In_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom In", style="BobwhiteRaisedButton.TButton", width=8, command = self.zoom_in_2)
            self.Zoom_Button_In_2.grid(row=2, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)        
            # Zoom Out
            self.Zoom_Button_Out_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom Out",  style="BobwhiteRaisedButton.TButton",width=8, command = self.zoom_out_2)
            self.Zoom_Button_Out_2.grid(row=3, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)         
            # Zoom Fit
            self.Zoom_Button_Fit_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom Fit", style="BobwhiteRaisedButton.TButton",width=8, command = self.zoom_fit_2)
            self.Zoom_Button_Fit_2.grid(row=4, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)       
            # Zoom 1/4
            self.Zoom_Button_025_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom 1/4", style="BobwhiteRaisedButton.TButton", width=8, command = self.zoom_to_quater_2)
            self.Zoom_Button_025_2.grid(row=5, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)         
            # Zoom 1/2
            self.Zoom_Button_05_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom 1/2", style="BobwhiteRaisedButton.TButton",width=8, command = self.zoom_to_half_2)
            self.Zoom_Button_05_2.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E) 
            # Zoom 1
            self.Zoom_Button_1_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom 1", style="BobwhiteRaisedButton.TButton",width=8, command = self.zoom_to_one_2)
            self.Zoom_Button_1_2.grid(row=7, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Zoom 2
            self.Zoom_Button_2_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom 2", style="BobwhiteRaisedButton.TButton",width=8, command = self.zoom_to_two_2)
            self.Zoom_Button_2_2.grid(row=8, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E) 
            # Zoom 4
            self.Zoom_Button_4_2 = ttk.Button(self.DS9_Button_Frame_2, text="Zoom 4", style="BobwhiteRaisedButton.TButton", width=8, command = self.zoom_to_four_2)
            self.Zoom_Button_4_2.grid(row=9, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteRaisedButton.TButton", width=10, command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=10, column=1, columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
            # Aperphot
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",   style="BobwhiteRaisedButton.TButton", width=10, command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=11, column=1, columnspan=2, padx=(0,0), pady=(3,3), sticky=E+W)
            self.pressed_zoom_count_2 = 1
        if self.Zoom_Style_2 == "BobwhiteSunkenButton.TButton":            
            self.Zoom_Button_2.configure(style="BobwhiteRaisedButton.TButton")
            self.reset_button_states_2()
            # Scale
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteRaisedButton.TButton", width=10, command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            # IRAF
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",  style="BobwhiteRaisedButton.TButton",  width=10, command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_zoom_count_2 = 0            
        return self.current_zoom_value_2, self.pressed_scale_count_2, self.pressed_aperphot_count_2

    def show_scale_options_2(self):
        self.Scale_Style_2 = self.Scale_Button_2['style']
        if self.Scale_Style_2 == "BobwhiteRaisedButton.TButton":                   
            self.reset_button_states_2()
            # Scale
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteSunkenButton.TButton", command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            # Scale Linear
            self.Scale_Linear_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Linear ",  style = "BobwhiteRaisedButton.TButton", width=8, command = self.scale_linear_2)
            self.Scale_Linear_2.grid(row=3, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale Log
            self.Scale_Log_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Log ",  style = "BobwhiteRaisedButton.TButton",  width=8,command = self.scale_log_2)
            self.Scale_Log_2.grid(row=4, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale MinMax
            self.Scale_MinMax_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Min Max ",  style = "BobwhiteRaisedButton.TButton", width=8, command = self.set_scale_minmax_2)
            self.Scale_MinMax_2.grid(row=5, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # Scale ZScale
            self.Scale_ZScale_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Zscale ",  style = "BobwhiteRaisedButton.TButton", width=8, command = self.set_scale_zscale_2)
            self.Scale_ZScale_2.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=(0,0), sticky=E)
            # IRAF
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",   style="BobwhiteRaisedButton.TButton", command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=7, column=1, columnspan=2, padx=(0,0), pady=(0,0), sticky=E+W)
            self.pressed_scale_count_2 = 1
        if self.Scale_Style_2 == "BobwhiteSunkenButton.TButton":
            self.Scale_Button_2.configure(style="BobwhiteRaisedButton.TButton")
            self.reset_button_states_2()
            # IRAF
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="RaisedButton.TButton", command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",  style="RaisedButton.TButton", command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_scale_count_2 = 0
        return self.current_zoom_value_2, self.pressed_scale_count_2, self.pressed_aperphot_count_2

    def show_aperphot_options_2(self):
        self.IRAF_Style_2 = self.Aperphot_Button_2['style']
        if self.IRAF_Style_2 == "BobwhiteRaisedButton.TButton":          
            self.reset_button_states_2()
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteRaisedButton.TButton", command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",  style="BobwhiteSunkenButton.TButton", command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            # Aperphot Imexamine a
            self.Imexamine_A_2 = ttk.Button(self.DS9_Button_Frame_2, text="AperPhot",  style = "BobwhiteRaisedButton.TButton", width=8,  command = self.imexamine_a_2)
            self.Imexamine_A_2.grid(row=4, column=1, columnspan=1, rowspan=1, padx=(5,0), pady=(0,0), sticky=E)
            self.pressed_aperphot_count_2 = 1
        if self.IRAF_Style_2 == "BobwhiteSunkenButton.TButton":
            self.Aperphot_Button_2.configure(style="BobwhiteRaisedButton.TButton")
            self.reset_button_states_2()
            self.Scale_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" Scale ",   style="BobwhiteRaisedButton.TButton", command = self.show_scale_options_2)
            self.Scale_Button_2.grid(row=2, column=0, columnspan=2, rowspan=1,padx=(0,0), pady=(2,2), sticky=E+W)
            self.Aperphot_Button_2 = ttk.Button(self.DS9_Button_Frame_2, text=" IRAF ",  style="BobwhiteRaisedButton.TButton", command = self.show_aperphot_options_2)
            self.Aperphot_Button_2.grid(row=3, column=0, columnspan=2, rowspan=1, padx=(0,0), pady=(2,2), sticky=E+W)
            self.pressed_aperphot_count_2 = 0
        return self.current_zoom_value_2, self.pressed_scale_count_2, self.pressed_aperphot_count_2

    def load_file_1(self, filepath):
        image = load_data(filepath, logger=self.logger)
        self.fitsimage_1.set_image(image)
        self.pan_center_value_1 = self.fitsimage_1.get_pan()
        self.zoom_fit_value_1 = self.fitsimage_1.get_zoom()
        self.current_zoom_value_1 = self.zoom_fit_value_1
        filepath1 = filepath.split("/")
        filepath2 = ""
        for i in range(1, (len(filepath1)-1)):
            filepath2 = filepath2 + "/" + filepath1[i]
            if i==3:
                filepath2 = filepath2 + "/"+ "\n"
        filepath2 = filepath2+ "/"+ "\n" + "/"+ filepath1[len(filepath1)-1]
        self.imstatistics_1(filepath)
        return self.pan_center_value_1, self.zoom_fit_value_1, self.current_zoom_value_1

    def open_file_1(self):        
        filename = askopenfilename(filetypes=[("allfiles", "*"),("fitsfiles", "*.fit"),("fitsfiles", "*.fits")])
        if not filename:
            pass
        else:
            self.load_file_1(filename)        

    def imstatistics_1(self,filepath):
        self.data_1 = fits.getdata(filepath)
        meanval = np.mean(self.data_1)
        self.meanval_1 = (int(meanval*100))/100
        stdval = np.std(self.data_1)
        self.stdval_1 = (int(stdval*100))/100
        self.minval_1 = np.min(self.data_1)
        self.maxval_1 = np.max(self.data_1)
        self.Mean_1.config(text=str(self.meanval_1))
        self.StdDev_1.config(text=str(self.stdval_1))
        self.Min_1.config(text=str(self.minval_1))
        self.Max_1.config(text=str(self.maxval_1))
        self.scale_bar_1 = np.linspace(self.minval_1, self.maxval_1, 111)
        if self.fig_1 != None:            
            plt.close(self.fig_1) 
        self.fig_1 = plt.figure(figsize=(6.2, 0.2))
        plt.imshow(self.data_1, cmap='gray')        
        return self.meanval_1, self.stdval_1, self.minval_1, self.maxval_1, self.scale_bar_1, self.data_1

    def load_file_2(self, filepath):
        image = load_data(filepath, logger=self.logger)
        self.fitsimage_2.set_image(image)
        self.pan_center_value_2 = self.fitsimage_2.get_pan()
        self.zoom_fit_value_2 = self.fitsimage_2.get_zoom()
        self.current_zoom_value_2 = self.zoom_fit_value_2        
        self.imstatistics_2(filepath)
        return self.pan_center_value_2, self.zoom_fit_value_2, self.current_zoom_value_2, self.minval_2, self.maxval_2

    def open_file_2(self):        
        filename = askopenfilename(filetypes=[("allfiles", "*"),("fitsfiles", "*.fit")])
        if not filename:
            pass
        else:
            self.load_file_2(filename)
            
    def imstatistics_2(self,filepath):
        self.data_2 = fits.getdata(filepath)
        meanval = np.mean(self.data_2)
        self.meanval_2 = (int(meanval*100))/100
        stdval = np.std(self.data_2)
        self.stdval_2 = (int(stdval*100))/100
        self.minval_2 = np.min(self.data_2)
        self.maxval_2 = np.max(self.data_2)
        self.Mean_2.config(text=str(self.meanval_2))
        self.StdDev_2.config(text=str(self.stdval_2))
        self.Min_2.config(text=str(self.minval_2))
        self.Max_2.config(text=str(self.maxval_2))
        self.scale_bar_2 = np.linspace(self.minval_2, self.maxval_2, 111)
        if self.fig_2 != None:            
            plt.close(self.fig_2) 
        self.fig_2 = plt.figure(figsize=(6.2, 0.2))
        plt.imshow(self.data_2, cmap='gray')        
        return self.meanval_2, self.stdval_2, self.minval_2, self.maxval_2, self.scale_bar_2, self.data_2, self.minval_2, self.maxval_2        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        
def main():
    root = Tk()    
    app = Camera_Options(root)
    root.mainloop()
   # root.destroy()    
    return 0


if __name__ == '__main__':
    main()

