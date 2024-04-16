from datetime import datetime
import re
import threading
import time
import queue
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
import queue
import numpy as np
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from os import path

class CameraThreadedClient(threading.Thread):
    def __init__(self, Queue_In, Queue_Out):
        threading.Thread.__init__(self)
        self.queue_in = Queue_In
        self.queue_out = Queue_Out
        self._stop_event = threading.Event()
        self.sensor_temp_value = None
        self.cooler_power_value = None
        self.heat_sink_value = None
        self.sensor_temp_value = None        
        self.heat_sink_value = None
        self.number_of_cameras = None
        self.running = True
        self.quit_command = 'NNNNNNNNNNNNNNNN~QUIT~'
        self.init_command = 'NNNNNNN-NNNNNNNN~INIT~'
        self.serials = []
        self.cmd = "/Users/observer/Desktop/QUAIL_soft/SBIG_drivers/Sample/SBIGDriver"
        self.init_cameras()
        
    def stop(self):
        self._stop_event.set()
        self.running = False        

    def stopped(self):
        return self._stop_event.is_set()

    def quit():
        self.p.stdin.write(quit_command)
        self.p.stdin.flush()        

    def init_cameras(self):        
        self.p = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT,  bufsize=1, encoding='utf8')        
        self.p.stdin.write(self.init_command)
        self.p.stdin.flush()
        line_0 =  self.p.stdout.readline()
        try:
            c = line_0.strip('camCount: ')
            c = c.strip('\n')
            self.number_of_cameras = int(c)
            for i in range(0,self.number_of_cameras):
                line_1 = self.p.stdout.readline()
                s = line_1.strip('Serial:')
                self.serial_number =  s.strip('\n')
                self.serials.append(self.serial_number)
        except:
            if "No USB cameras found" in line_0:
                self.running = False
                self.p.stdin.write(quit_command)
                self.p.stdin.flush()
        return self.serials, self.number_of_cameras
       
    def read_query_result(self, result):
        result = result
        result = result.strip('QUERY: ')
        result = result.split(']')
        result[0] = result[0].strip('[')
        result[1] = result[1].strip('[')
        result[2] = result[2].strip('[')
        result[3] = result[3].strip('[')
        result[4] = result[4].strip('[')
        serial = result[0].strip("Serial:") 
        self.CCD_temp = result[1].strip('Sensor Temperature:')
        self.cooler_power = result[2].strip('Cooler Power:')
        self.heat_sink_temp = result[3].strip('Heat Sink Temperature:')
        self.main_sensor_state = result[4].strip('Main Sensor State:')
        return self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state

    def check_query(self, line):
        line_0 = line
        if "QUERY:" in line_0:
            result = line_0
            self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.read_query_result(result)
        return self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state
        
    def run(self):        
        while self.running==True:
            if self.queue_in.qsize()>0:
                msg = self.queue_in.get()
                print("thread msg", msg)                
                try:
                    # INIT and QUIT are unique
                    if msg[0] == "INIT":                    
                        self.serials, self.number_of_cameras, self.itercycle = self.init_cameras()
                        self.queue_out.put(["INIT", self.serials])
                    elif msg[0] == "QUIT":
                        quit_command = 'AL3200M-18070401~QUIT~'                    
                        self.p.stdin.write(quit_command)
                        self.p.stdin.flush()
                        self.running = False
                    else:
                        camcount = 0
                        query_result = []                        
                        for i in self.itercycle:
                            if msg[i] == "QUERY":
                                query_camera = msg[i+1]
                                query_command = query_camera + '~QUER~'
                                self.p.stdin.write(query_command)
                                self.p.stdin.flush()
                                line_0 = self.p.stdout.readline()
                                self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.check_query(line_0)
                                query_result.append("QUERY")
                                query_result.append(self.serials[camcount])
                                query_result.append(self.CCD_temp)
                                query_result.append(self.cooler_power)
                                query_result.append(self.heat_sink_temp)
                                query_result.append(self.main_sensor_state)                                    
                            elif msg[i] == "COOL":
                                cool_camera = msg[i+1]
                                cool_command = cool_camera
                                self.p.stdin.write(cool_command)
                                self.p.stdin.flush()
                                line_0 = self.p.stdout.readline()
                                self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.check_query(line_0)
                                query_result.append("QUERY")
                                query_result.append(self.serials[camcount])
                                query_result.append(self.CCD_temp)
                                query_result.append(self.cooler_power)
                                query_result.append(self.heat_sink_temp)
                                query_result.append(self.main_sensor_state)
                            elif msg[i] == "EXPOSE":
                                expose_command = msg[i+1]                                
                                self.p.stdin.write(expose_command)
                                self.p.stdin.flush()
                                line_0 = self.p.stdout.readline()
                                self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.check_query(line_0)
                                query_result.append("QUERY")
                                query_result.append(self.serials[camcount])
                                query_result.append(self.CCD_temp)
                                query_result.append(self.cooler_power)
                                query_result.append(self.heat_sink_temp)
                                query_result.append(self.main_sensor_state)                                    
                            elif msg[i] == "READOUT":
                                readout_command = msg[i+1]
                                self.p.stdin.write(readout_command)
                                self.p.stdin.flush()
                                line_0 = self.p.stdout.readline()                                
                                self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.check_query(line_0)
                                query_result.append("QUERY")
                                query_result.append(self.serials[camcount])
                                query_result.append(self.CCD_temp)
                                query_result.append(self.cooler_power)
                                query_result.append(self.heat_sink_temp)
                                query_result.append(self.main_sensor_state)                                
                            elif msg[i] == "ABORT":
                                abort_command = msg[i+1]
                                self.p.stdin.write(abort_command)
                                self.p.stdin.flush()
                                line_0 = self.p.stdout.readline()
                                self.CCD_temp, self.cooler_power, self.heat_sink_temp, self.main_sensor_state = self.check_query(line_0)
                                query_result.append("QUERY")
                                query_result.append(self.serials[camcount])
                                query_result.append(self.CCD_temp)
                                query_result.append(self.cooler_power)
                                query_result.append(self.heat_sink_temp)
                                query_result.append(self.main_sensor_state)                                
                            elif msg[i] == "WAIT":
                                pass
                            else:
                                pass                                                           
                            camcount=camcount+1
                        self.queue_out.put(query_result)                   
                except:
                    quit_command = '~QUIT~'
                    self.p.stdin.write(quit_command)
                    self.p.stdin.flush()
                    self.running = False

















            

            
