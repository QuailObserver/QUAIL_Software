#include "fitsio.h" /* required by every program that uses CFITSIO */
#include <fstream>
#include "dlapi.h"

#include <chrono>
#include <iostream>
#include <thread>
#include <cinttypes>

#include <errno.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/filio.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include "fitsio.h"

#include <fcntl.h>
#include <string>
#include <vector>
#include<cmath>
#include <iomanip>

using namespace dl;
using namespace std::chrono_literals;

std::string getSerial(ICameraPtr pCamera)
{
	char buf[512] = {0};
	size_t blng = 512;
	pCamera->getSerial(&(buf[0]), blng);
	return std::string(&(buf[0]), blng);
}


void handlePromise(IPromisePtr pPromise)
{
	auto result = pPromise->wait();
	if (result != IPromise::Complete)
	{
		char b[512] = {0};
		size_t l = 512;
		pPromise->getLastError(&(b[0]), l);
		pPromise->release();
		throw std::logic_error(std::string(&(b[0]), l));
	}
}

std::string setpoint_settings(ICameraPtr pCamera, int toggle_cooling, float setpoint)
{	//int toggle_cooling = atoi(argv[1]);
	//float setpoint = atoi(argv[2]);
	ICamera::Status status;
	auto pITEC = pCamera->getTEC();              									// Creates Handle for TEC stuff 	   
	handlePromise(pITEC->setState(toggle_cooling,setpoint));  
	handlePromise(pCamera->queryStatus());
	status = pCamera->getStatus();	
	float sensortemperature = status.sensorTemperature;
	float coolerpower = status.coolerPower;
	float heatsinktemperature = status.heatSinkTemperature;
	int mainsensorstate = status.mainSensorState;
	bool enabled = pITEC->getEnabled();
	auto serial  = getSerial(pCamera);
	std::string status_string = "[Serial:" + serial+ "]";
	status_string = status_string + "[Sensor Temperature:" + std::to_string(sensortemperature)+"]";
	status_string = status_string + "[Cooler Power:" + std::to_string(coolerpower)+"]"; 
	status_string = status_string + "[Heat Sink Temperature:" + std::to_string(heatsinktemperature)+"]";
	status_string = status_string + "[Main Sensor State:" + std::to_string(mainsensorstate)+"]";
	status_string = status_string + "[Cooling:" + std::to_string(enabled)+"]";
	return status_string;
}

std::string query_settings(ICameraPtr pCamera)
{
	ICamera::Status status;
	handlePromise(pCamera->queryStatus());
	status = pCamera->getStatus();
	auto pITEC = pCamera->getTEC();   
	//std::string status_string = "";  
	float sensortemperature = status.sensorTemperature;
	float coolerpower = status.coolerPower;
	float heatsinktemperature = status.heatSinkTemperature;
	int mainsensorstate = status.mainSensorState;
	bool enabled = pITEC->getEnabled();
	auto serial  = getSerial(pCamera);
	//std::cout<< "query enabled" << enabled << std::endl;
	std::string status_string = "[Serial:" + serial+"]";
	status_string = status_string + "[Sensor Temperature:" + std::to_string(sensortemperature)+"]";
	status_string = status_string + "[Cooler Power:" + std::to_string(coolerpower)+"]"; 
	status_string = status_string + "[Heat Sink Temperature:" + std::to_string(heatsinktemperature)+"]";
	status_string = status_string + "[Main Sensor State:" + std::to_string(mainsensorstate)+"]";
	status_string = status_string + "[Cooling:" + std::to_string(enabled)+"]";
	return status_string;
}



int main()

{
    //CHANGES
    
    auto pGateway = getGateway();
	try
	{
		// find all USB cameras connected to this computer
		pGateway->queryUSBCameras();
		// count how many there are
		auto camCount = pGateway->getUSBCameraCount();
        std::cout << "camCount: " << camCount << std::endl;
        
        // Initialize our variables used to listen to user input
		char c[256];
		int n1;
		int tem;
		int cnt = 0;	
        char delimiter[] ={'~','\0'};		

        char decimal_delimiter[] ={'.','\0'};		
        
		char command[4];				
		char command_quit[] = {'Q','U','I','T','\0'};
		char command_query[] = {'Q','U','E','R','\0'};
		char command_cool[] = {'C','O','O','L','\0'};
		char command_stop_cool[] = {'S','T','C','L','\0'};
		char command_expose[] = {'E','X','P','S','\0'};
		char command_abort[] = {'A','B','R','T','\0'};	
		char command_readout[] = {'R','D','O','T','\0'};
		char command_init[] = {'I','N','I','T','\0'};	
		char parameters;
        std::vector<std::string> serial_numbers;

		bool is_quit_issued = strcmp(command, command_quit);	
        bool is_init_issued = strcmp(command, command_init);
        bool is_cool_issued = strcmp(command, command_cool);
        bool is_query_issued = strcmp(command, command_query);
        bool is_abort_issued = strcmp(command, command_abort);
        bool is_expose_issued = strcmp(command, command_expose);
        bool is_readout_issued = strcmp(command, command_readout);

        
		is_quit_issued = 1;
		int is_exposure_going = 0;
		int m;


        while (is_quit_issued == 1)
		{
			tem = fcntl(0, F_GETFL, 0);
			fcntl (0, F_SETFL, (tem | O_NDELAY));
			n1 = read(0, &c, 256);
			while (n1 <= 0)
			{	
				n1 = read(0, &c, 256);	
				if (is_exposure_going == 1)
				{	std::this_thread::sleep_for(50ms);					
				}
				if (is_exposure_going == 0)
				{
					std::this_thread::sleep_for(50ms);					
				}							
				if (n1 > 0)
				{	break;
				}
			}

            // find where delimeters are
            m = 0;
            int foo[256]; //this is the locations of delimeters
            int count = 0;            
            for (m=0; m<256; ++m)
			{
                char a[] = {c[m], '\0'};                
                 if (strcmp(a,delimiter)==0)
                {
                  foo[count] = m;
                  count = count+1;
                }
			}	
            // init serial
            //char serial_number[foo[0]];
            std::string serial_number = "";
            m=0;
            for (m=0; m<(foo[0]); ++m)
            {
                serial_number = serial_number + c[m];
            }
            //serial_number[foo[0]] = ('\0');	
           // std::cout<<"Serial: "<< serial_number << std::endl;

            // init command
            count=0;
            int command_size = foo[1] - foo[0];
            char command[command_size];            
            for (m=(foo[0]+1); m<(foo[1]); ++m)
            {
                command[count] = c[m];
                count = count+1;
            }
            command[command_size-1] = ('\0');	
           // std::cout<<"command: "<< command<< std::endl;


                // if a QUIT command is issued halt the program
                is_quit_issued = strcmp(command, command_quit);		
                if 	(is_quit_issued ==0)
                {	return EXIT_SUCCESS;
                }


                // if INIT is issued retriee serial numbers and store them in an array
                is_init_issued = strcmp(command, command_init);		
                if 	(is_init_issued ==0)
                {	
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                        auto pCamera = pGateway->getUSBCamera(m);
                        if (!pCamera)
                        {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                            return EXIT_FAILURE;
                        }
                        std::string serial = getSerial(pCamera);
                        // std::string serial = std::to_string(m);
                            //strcpy(serial_numbers[m],serial.c_str());
                        serial_numbers.push_back(serial);
                        std::cout << "Serial:" << serial_numbers[m] << std::endl;
                                            
                        }
                             
                       // std::cout << "serial_numbers[1]"<< serial_numbers[1] << std::endl;  
                        is_init_issued = 1;
                    }
                }	


                // If Cool Is Issued
                is_cool_issued = strcmp(command, command_cool);
                if (is_cool_issued == 0)
                {
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    m=0;
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                            auto pCamera = pGateway->getUSBCamera(m);
                            if (!pCamera)
                            {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                                return EXIT_FAILURE;
                            }
                            
                            std::string serial = getSerial(pCamera);
                            if (serial_number.compare(serial) == 0)
                            {
                                auto pSensor = pCamera->getSensor(0);                                
                                if (!pSensor)
                                {	std::cout << "Sensor could not be retrieved from Camera" << std::endl;
                                    return 1;
                                }
                                // parse parameters
                                // Enable/Disable cooling
                                // if Enable (1) then the next parameter is the sign (+/-) AL3200M-18070201~COOL~1~+~05~
                                // if Disable then the rest doesn't matter
                                // the temperature parameters are integers with length 1 or two. 
                                int toggle_cooling = (int)c[foo[1]+1] - 48;
                                std::string plusminus(1, c[foo[2]+1]);                                
                                int temp1 = 10*((int)(c[foo[3]+1]) - 48);
                                int temp2 = (int)(c[foo[3]+2]) - 48;
                                float temperature = temp1 + temp2;
                                
                                if (plusminus.compare("-")== 0)
                                {
                                    temperature = -1*temperature;
                                }
                            // std::cout << toggle_cooling<< std::endl;
                            // std::cout << temperature << std::endl;
                                std::string cooling_result = setpoint_settings(pCamera, toggle_cooling,temperature);
                                std::cout << "QUERY: " << cooling_result <<std::endl;
                                is_cool_issued = 1;
                            }
                        }
                    }
                }


                // If QUERY is issued
                is_query_issued = strcmp(command, command_query);
                if (is_query_issued==0)
                {
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    m=0;
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                            auto pCamera = pGateway->getUSBCamera(m);
                            if (!pCamera)
                            {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                                return EXIT_FAILURE;
                            }
                            std::string serial = getSerial(pCamera);
                            if (serial_number.compare(serial) == 0)
                            {
                                auto pSensor = pCamera->getSensor(0);
                                if (!pSensor)
                                {	std::cout << "Sensor could not be retrieved from Camera" << std::endl;
                                    return 1;
                                }
                            auto result_settings = query_settings(pCamera);	
                            std::cout << "QUERY: " << result_settings <<std::endl; 
                            is_query_issued = 1;
                            }
                        }
                    }
                }


                // If ABORT is issued
                is_abort_issued = strcmp(command, command_abort);
                if (is_abort_issued==0)
                {
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    m=0;
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                            auto pCamera = pGateway->getUSBCamera(m);
                            if (!pCamera)
                            {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                                return EXIT_FAILURE;
                            }
                            std::string serial = getSerial(pCamera);
                            if (serial_number.compare(serial) == 0)
                            {
                                auto pSensor = pCamera->getSensor(0);
                                if (!pSensor)
                                {	std::cout << "Sensor could not be retrieved from Camera" << std::endl;
                                    return 1;
                                }
                                auto sInfo = pSensor->getInfo();
                                handlePromise(pSensor->abortExposure());	
                                is_exposure_going = 0;	
                                auto result_settings = query_settings(pCamera);	
                                std::cout << "QUERY: " << result_settings <<std::endl; //setpoint_settings
                                is_abort_issued = 1;
                            }
                        }
                    }
                }
                








                // If EXPOSE is issued
                is_expose_issued = strcmp(command, command_expose);
                if (is_expose_issued==0)
                {
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    m=0;
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                            auto pCamera = pGateway->getUSBCamera(m);
                            if (!pCamera)
                            {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                                return EXIT_FAILURE;
                            }
                            std::string serial = getSerial(pCamera);
                            if (serial_number.compare(serial) == 0)
                            {
                                auto pSensor = pCamera->getSensor(0);
                                if (!pSensor)
                                {	std::cout << "Sensor could not be retrieved from Camera" << std::endl;
                                    return 1;
                                }
                                auto sInfo = pSensor->getInfo();	
                                is_exposure_going = 1;	
                                // xbin, ybin, top, left, exposure_time, frametype, readout, overscan, rbi_preflash_duration, rbi_clearouts
                                int bin_x = (int)c[foo[1]+1] - 48;
                                int bin_y = (int)c[foo[2]+1] - 48;
                                // Top Offset
                                int offset_size = foo[4] - foo[3];
                                int count = offset_size - 2;     
                                m=0;      
                                int top = 0;
                                for (m=(foo[3]+1); m<(foo[4]); ++m)
                                {
                                    top = top + (int)(c[m]-48)*pow(10, count);
                                    count = count-1;
                                }
                              // std::cout<< "top:" << top<<std::endl;

                                // left offset
                                offset_size = foo[5] - foo[4];
                                count = offset_size - 2;     
                                m=0;      
                                int left = 0;
                                for (m=(foo[4]+1); m<(foo[5]); ++m)
                                {
                                    left = left + (int)(c[m]-48)*pow(10, count);
                                    count = count-1;
                                }
                            //   std::cout<< "left:"<<left<<std::endl;
                               // EXPOSUUUREEEE
                               // find out where the "." is to delimeter the ints from floats
                               int exp_size = foo[6] - foo[5];
                               m=0;
                               float exposure_time;
                               int decimal_location;
                               for (m=(foo[5]+1); m<(foo[6]); ++m)
                                {
                                    char a[] = {c[m], '\0'};               
                                    if (strcmp(a,decimal_delimiter)==0)
                                    {
                                         decimal_location = m;
                                    }
                                }	
                              //  std::cout<< "decimal_location 1:" <<decimal_location << std::endl;
                                // now parse and add exposure time
                                int int_size = decimal_location - foo[5];
                                if (decimal_location>0)
                                {                                
                                count = int_size - 2;     
                                m=0;      
                                int int_exp = 0;
                                for (m=(foo[5]+1); m<(decimal_location); ++m)
                                {
                                    int_exp = int_exp + (int)(c[m]-48)*pow(10, count);
                                    count = count-1;
                                }
                               int_size = foo[6] - decimal_location;
                               count = 1;
                               m=0;
                               float dec_exp = 0;
                               for (m=(decimal_location+1); m<(foo[6]); ++m)
                                {
                                    dec_exp = dec_exp + (int)(c[m]-48)/(pow(10, count));
                                    count = count+1;
                                }
                                exposure_time = int_exp + dec_exp;
                                
                                }
                                if (decimal_location<=0)
                                {
                                    int_size = exp_size;
                                    count = int_size - 2;     
                                    m=0;      
                                    int int_exp = 0;
                                    for (m=(foo[5]+1); m<(foo[6]); ++m)
                                    {
                                        int_exp = int_exp + (int)(c[m]-48)*pow(10, count);
                                        count = count-1;
                                    }
                                    exposure_time = int_exp + 0.00;
                                }
                               //std::cout << "exposure_time:" << exposure_time << std::endl;
                                // frametype
                                int frametype = (int)c[foo[6]+1] - 48;
                                // readout
                                int readout = (int)c[foo[7]+1] - 48;
                                // overscan
                                int overscan = (int)c[foo[8]+1] - 48;
                                // RBI preflash duration
                                // RBIIIII
                                // find out where the "." is to delimeter the ints from floats
                                exp_size = foo[10] - foo[9];
                                m=0;
                                decimal_location = 0;
                               for (m=(foo[9]+1); m<(foo[10]); ++m)
                                {
                                    char a[] = {c[m], '\0'};               
                                    if (strcmp(a,decimal_delimiter)==0)
                                    {
                                         decimal_location = m;
                                    }
                                }	
                                // AL3200M-18070401~EXPS~1~1~0~0~0~1~1~1~0~0~
                                

                               // std::cout<< "decimal_location:" <<decimal_location << std::endl;
                                // now parse and add exposure time
                                float rbi_preflash_duration;
                                if (decimal_location>0)
                                {
                                    int_size = decimal_location - foo[9];
                                    count = int_size - 2;     
                                    m=0;      
                                    int int_rbi = 0;
                                    for (m=(foo[9]+1); m<(decimal_location); ++m)
                                    {
                                        int_rbi = int_rbi + (int)(c[m]-48)*pow(10, count);
                                        count = count-1;
                                    }
                                    int_size = foo[10] - decimal_location;
                                    count = 1;
                                    m=0;
                                    float dec_rbi = 0;
                                    for (m=(decimal_location+1); m<(foo[10]); ++m)
                                    {
                                        dec_rbi = dec_rbi + (int)(c[m]-48)/(pow(10, count));
                                        count = count+1;
                                    }
                                    rbi_preflash_duration = int_rbi + dec_rbi;
                                }
                                if (decimal_location<=0)
                                {
                                    int_size = foo[10] - foo[9];
                                    count = int_size - 2;     
                                    m=0;      
                                    int int_rbi = 0;
                                    for (m=(foo[9]+1); m<(foo[10]); ++m)
                                    {
                                        int_rbi = int_rbi + (int)(c[m]-48)*pow(10, count);
                                        count = count-1;
                                    }
                                    rbi_preflash_duration = int_rbi + 0.00;
                                }
                               //  std::cout << "rbi_preflash_duration:" << rbi_preflash_duration << std::endl;
                                 
                                 // rbi flushes
                                 offset_size = foo[11] - foo[10];
                                 count = offset_size - 2;     
                                 m=0;      
                                 int number_of_flushes = 0;
                                 for (m=(foo[10]+1); m<(foo[11]); ++m)
                                 {
                                     number_of_flushes = number_of_flushes + (int)(c[m]-48)*pow(10, count);
                                     count = count-1;
                                 }
                           //     std::cout<< "number_of_flushes:" << number_of_flushes<<std::endl;
                                // toggle IR LEDs
                                bool rbi = 0;
                                if (rbi_preflash_duration>0)
                                {
                                    rbi = true;
                                }
                             //   std::cout<< "RBI LEDs On/Off:" << rbi <<std::endl;

                                //set up subframe
                                TSubframe sf;
                                sf.binX = bin_x;
                                sf.binY = bin_y;	
                                sf.top = top;
                                sf.left = left;
                                sf.width = (sInfo.pixelsX/bin_x);
                                sf.height = (sInfo.pixelsY/bin_y);	
                                handlePromise(pSensor->setSubframe(sf)); 
                                // set up exposure options
                               // std::cout<< "c" << c << std::endl;
                                TExposureOptions eo;                                      // Exposure options
                                eo.duration = exposure_time;
                                eo.isLightFrame = frametype;
                                eo.readoutMode = readout;
                                eo.useRBIPreflash = rbi;
                                // Miscellaneous Settings
                                handlePromise(pSensor->setSetting(ISensor::Setting::UseOverscan, overscan));
                                handlePromise(pSensor->setSetting(ISensor::Setting::RBIPreflashDuration, rbi_preflash_duration));
                                handlePromise(pSensor->setSetting(ISensor::Setting::RBIPreflashFlushCount, number_of_flushes));
                                handlePromise(pSensor->setSetting(ISensor::Setting::UseOnChipBinning, 0)); // on chip binning des nothing...deprecated?
                                handlePromise(pSensor->startExposure(eo)); 		
                                
                               auto result_settings = query_settings(pCamera);	
                               std::cout << "QUERY: " << result_settings <<std::endl; 	
                               is_expose_issued = 1;			    
                            }
                         }
                     }
                 }


                // If READOUT is issued
                is_readout_issued = strcmp(command, command_readout);
                if (is_readout_issued==0)
                {
                    if (camCount==0)
                    {
                        std::cout << "No USB Cameras Found" << std::endl;
                        return EXIT_FAILURE;
                    }
                    m=0;
                    if (camCount >0)
                    {   m=0;
                        for (m=0; m<camCount; ++m)
                        {
                            auto pCamera = pGateway->getUSBCamera(m);
                            if (!pCamera)
                            {	std::cout << "Camera could not be retrieved from Gateway" << std::endl;
                                return EXIT_FAILURE;
                            }
                            std::string serial = getSerial(pCamera);
                            if (serial_number.compare(serial) == 0)
                            {
                                auto pSensor = pCamera->getSensor(0);
                                if (!pSensor)
                                {	std::cout << "Sensor could not be retrieved from Camera" << std::endl;
                                    return 1;
                                }
                                handlePromise(pSensor->startDownload());
                                auto pImg = pSensor->getImage();
                                auto pData = pImg->getBufferData();
                                auto lng = pImg->getBufferLength();
                                uint16_t * pBuffer = new uint16_t[lng]; 		
                                memcpy(pBuffer, pData, sizeof(uint16_t)*lng);
                                //std::cout << "Got Data" << std::endl;

                            
                                auto timd = pImg->getMetadata();
                                int image_width = timd.width;
                                int image_height = timd.height;
                                //std::cout<< image_width << std::endl;
                                int offset_x = timd.offsetX;
                                int offset_y = timd.offsetY;
                                int bin_x = timd.binX +1;
                                int bin_y = timd.binY + 1;
                                float gain = timd.eGain;
                                float exposure_duration = timd.exposureDuration;

                               // std::cout << image_width << image_height << std::endl;

                                int overscan = (int)c[foo[1]+1] - 48;
                                // std::cout << "c" << c << std::endl;
                               // std::cout << "overscan:" << overscan << std::endl;
                                // frame type
                                std::string frametype = "";
                                m=0;
                                for (m=(foo[2]+1); m<(foo[3]); ++m)
                                {
                                   frametype = frametype + c[m];
                                }
                                  //      std::cout << "frametype:" << frametype << std::endl;
                                // camera name
                                std::string camera_name = "";
                                m=0;
                                for (m=(foo[3]+1); m<(foo[4]); ++m)
                                {
                                   camera_name = camera_name + c[m];
                                }
                                 //   std::cout << "camera_name:" << camera_name << std::endl;
                                // object name
                                std::string object_name = "";
                                m=0;
                                for (m=(foo[4]+1); m<(foo[5]); ++m)
                                {
                                   object_name = object_name + c[m];
                                }
                                // std::cout << "object_name:" << object_name << std::endl;
                                
                                // filter type
                                std::string filter_type = "";
                                m=0;
                                for (m=(foo[5]+1); m<(foo[6]); ++m)
                                {
                                   filter_type = filter_type + c[m];
                                }
                               //    std::cout << "filter_type:" << filter_type << std::endl;
                                
                                // LMST
                                std::string LMST = "";
                                m=0;
                                for (m=(foo[6]+1); m<(foo[7]); ++m)
                                {
                                   LMST = LMST + c[m];
                                }
                              //    std::cout << "LMST:" << LMST << std::endl;

                                // RA
                                std::string RA = "";
                                m=0;
                                for (m=(foo[7]+1); m<(foo[8]); ++m)
                                {
                                   RA = RA + c[m];
                                }
                                //  std::cout << "RA:" << RA << std::endl;

                                // DEC
                                std::string DEC = "";
                                m=0;
                                for (m=(foo[8]+1); m<(foo[9]); ++m)
                                {
                                   DEC = DEC + c[m];
                                }
                                //  std::cout << "DEC:" << DEC << std::endl;
                                
                                // HA
                                std::string HA = "";
                                m=0;
                                for (m=(foo[9]+1); m<(foo[10]); ++m)
                                {
                                   HA = HA + c[m];
                                }
                                  //        std::cout << "HA:" << HA << std::endl;
                                
                                // Ambient Temperature
                                std::string ambient_plusminus(1, c[foo[10]+1]);                                
                                int ambient_temp1 = 10*((int)(c[foo[10]+2]) - 48);
                                int ambient_temp2 = (int)(c[foo[10]+3]) - 48;
                                //std::string ambient_dot(1, c[foo[10]+4]); 
                                int ambient_temp3 = (int)(c[foo[10]+5]) - 48;
                                float ambient_temperature = ambient_temp1 + ambient_temp2 + (0.1*ambient_temp3);
                                if (ambient_plusminus.compare("-")== 0)
                                {
                                    ambient_temperature = -1*ambient_temperature;
                                }
                               //    std::cout << "ambient_temperature:" << ambient_temperature << std::endl;
                               
                                // birger
                                int birger1 = (10000)*((int)c[foo[11]+1] - 48); //1
                                int birger2 = (1000)*((int)c[foo[11]+2] - 48); //2
                                int birger3 = (100)*((int)c[foo[11]+3] - 48); //3
                                int birger4 = (10)*((int)c[foo[11]+4] - 48); //4
                                int birger5 = (1)*((int)c[foo[11]+5] - 48); //5
                                int birger = birger1 + birger2 + birger3 + birger4 + birger5;

                                auto result_settings = query_settings(pCamera);	                            
                               
                                 //      std::cout << "birger:" << birger << std::endl;
                                // filename
                                count=0;
                                int cs = foo[13] - foo[12];
                                char Filename[cs];            
                                for (m=(foo[12]+1); m<(foo[13]); ++m)
                                {
                                    Filename[count] = c[m];
                                    count = count+1;
                                }
                                Filename[cs-1] = ('\0');
                                

                                // sensor temp, etc
                                ICamera::Status status;
                                handlePromise(pCamera->queryStatus());
                                status = pCamera->getStatus(); 
                                float sensortemperature = status.sensorTemperature;
                            
                                fitsfile *fptr; /* pointer to the FITS file; defined in fitsio.h */
                                int fits_status, ii, jj;
                                long fpixel = 1, naxis = 2, nelements, exposure;
                              

                                uint16_t Data [image_height][image_width];
                                long naxes[2] = { image_width, image_height }; /* image is WIDTH pixels wide by HEIGHT rows */
                                fits_status = 0; /* initialize status before calling fitsio routines */
                                fits_create_file(&fptr, Filename, &fits_status); /* create new file */
                                /* Create the primary array image (16-bit short integer pixels */
                                fits_create_img(fptr, SHORT_IMG, naxis, naxes, &fits_status);
                            
                                // std::cout << "3" << std::endl;
                            
                                nelements = naxes[0] * naxes[1];
                                int n = 0;
                                // Average
                                double avg = 0;
                                int max = pBuffer[0];
                                int min = pBuffer[0];
                                for (jj = 0; jj < image_height; jj++)
                                {
                                    for (ii = 0; ii < image_width; ii++)
                                    {
                                        
                                        avg += pBuffer[n];
                                        if(pBuffer[n] > max)
                                             {max = pBuffer[n];}
                                        if(pBuffer[n] < min)
                                             {min = pBuffer[n];}
                                       // if (Data[jj][ii]< 0)
                                      //  {std::cout<< Data[jj][ii]<<std::endl;}
                                        if (pBuffer[n]>= 65535)
                                        {Data[jj][ii] = 65500;
                                        } else{
                                         Data[jj][ii] = pBuffer[n];
                                        }
                                        n = n+1;
                                    }
                                    
                                }
                                avg /= lng;
                                delete[] pBuffer;
                                fits_write_img(fptr, TSHORT, fpixel, nelements, Data[0], &fits_status);

                                fits_update_key(fptr, TDOUBLE, "MEAN", &avg, "Mean", &fits_status);
                                fits_update_key(fptr, TINT, "MAX", &max, "Max", &fits_status);
                                fits_update_key(fptr, TINT, "MIN", &min, "MIN", &fits_status);
                                fits_update_key(fptr, TINT, "XBINNING", &bin_x, "x-binning", &fits_status);
                                fits_update_key(fptr, TINT, "YBINNING", &bin_y, "y-binning", &fits_status);
                                fits_update_key(fptr, TFLOAT, "GAIN", &gain, "eGain", &fits_status);
                                fits_update_key(fptr, TFLOAT, "AMBTEMP", &ambient_temperature, "Ambient Temperature", &fits_status);
                                fits_update_key(fptr, TFLOAT, "CCDTEMP", &sensortemperature, "CCD Temperature", &fits_status);
                                fits_update_key(fptr, TSTRING, "IMAGETYP", &frametype, "Frame Type", &fits_status);
                                fits_update_key(fptr, TSTRING, "CAMNAME", &camera_name, "Camera Name", &fits_status);
                                fits_update_key(fptr, TSTRING, "SERIAL", &serial, "Serial Number", &fits_status);
                                fits_update_key(fptr, TSTRING, "FILTER", &filter_type, "Filter", &fits_status);
                                fits_update_key(fptr, TSTRING, "Object", &object_name, "Object", &fits_status);
                                fits_update_key(fptr, TSTRING, "LMST", &LMST, "LMST", &fits_status);
                                fits_update_key(fptr, TSTRING, "RA", &RA, "RA", &fits_status);
                                fits_update_key(fptr, TSTRING, "DEC", &DEC, "DEC", &fits_status);
                                fits_update_key(fptr, TSTRING, "HA", &HA, "HA", &fits_status);
                                fits_update_key(fptr, TINT, "BIRGER", &birger, "Focus Setpoint", &fits_status);
                                fits_update_key(fptr, TFLOAT, "EXPOSURE", &exposure_duration, "Total Exposure Time", &fits_status);
                                fits_close_file(fptr, &fits_status); /* close the file */
                                fits_report_error(stderr, fits_status); /* print out any error messages */   

                                                       
                                std::cout << "QUERY: " << result_settings <<std::endl; 
                               // is_exposure_going = 0;    
                                is_readout_issued = 1; 
                            
                            }
                        }
                    }
                }


            
    


        }
        
    } catch(const std::exception& e)
	{
		std::cerr << e.what() << '\n';
	}
	
	deleteGateway(pGateway);
	return 0;
// AL3200M-18070401~QUIT~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
// AL3200M-18070401~INIT~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
// AL3200M-18070401~COOL~1~-~10~efghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
// AL3200M-18070401~QUER~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
// AL3200M-18070401~ABRT~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
// AL3200M-18070401~EXPS~3~3~0~0~123456.0.12~1~1~1~3333~111~tqvwxy

// AL3200M-18070401~EXPS~1~1~0~0~3.12~1~1~1~0~0~
// AL3200M-18070401~EXPS~1~1~0~0~0.12~0~0~0~0~0~

// AL3200M-18070401~EXPS~1~1~0~0~2~1~1~1~0~0~

// AL3200M-18070401~QUER~abcdefghijklmnopqrstqvwxyzABCDEFGHIJKLMNO
 // AL3200M-18070401~RDOT~1~LIGHT~HARLEQUIN~OBJECT~FILTER~LMST~RA~DEC~HA~+22.2~21386~su2k1a.fits~
 // AL3200M-18070401~RDOT~1~LIGHT~HARLEQUIN~OBJECT~FILTER~LMST~RA~DEC~HA~+22.2~21386~su2k1a.fits~

// AL3200M-18070201~EXPS~1~1~0~0~2~1~1~1~0~0~
// AL3200M-18070201~QUER~
// AL3200M-18070401~QUER~
// AL3200M-18070201~RDOT~1~LIGHT~HARLEQUIN~OBJECT~FILTER~LMST~RA~DEC~HA~+22.2~21386~su22k1a.fits~
// AL3200M-18070201~QUER~
// AL3200M-18070201~QUIT~

// AL3200M-18070401~EXPS~1~1~0~0~2~1~1~1~0~0~
// AL3200M-18070201~QUER~
// AL3200M-18070401~QUER~
// AL3200M-18070401~RDOT~1~LIGHT~HARLEQUIN~OBJECT~FILTER~LMST~RA~DEC~HA~+22.2~21386~su11s2a.fits~
// AL3200M-18070201~QUER~
// AL3200M-18070201~QUIT~

// fitsfile *fptr; /* pointer to the FITS file; defined in fitsio.h */
// int status, ii, jj;
// long fpixel = 1, naxis = 2, nelements, exposure;
// long naxes[2] = { 300, 200 }; /* image is 300 pixels wide by 200 rows */
// short array[200][300];
// status = 0; /* initialize status before calling fitsio routines */
// fits_create_file(&fptr, "testfile.fits", &status); /* create new file */
// /* Create the primary array image (16-bit short integer pixels */
// fits_create_img(fptr, SHORT_IMG, naxis, naxes, &status);
// /* Write a keyword; must pass the ADDRESS of the value */
// exposure = 1500.;
// fits_update_key(fptr, TLONG, "EXPOSURE", &exposure,
// "Total Exposure Time", &status);
// /* Initialize the values in the image with a linear ramp function */
// for (jj = 0; jj < naxes[1]; jj++)
// for (ii = 0; ii < naxes[0]; ii++)
// array[jj][ii] = ii + jj;
// nelements = naxes[0] * naxes[1]; /* number of pixels to write */
// /* Write the array of integers to the image */
// fits_write_img(fptr, TSHORT, fpixel, nelements, array[0], &status);
// fits_close_file(fptr, &status); /* close the file */
// fits_report_error(stderr, status); /* print out any error messages */
// return( status );

}