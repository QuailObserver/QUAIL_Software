
from math import sin, cos, tan, pi, asin, acos, sqrt, atan
import time
import datetime

# constants for YUO, should be editable for other software tools
LATITUDE = 43.775
LONGITUDE = -79.5


# ==============================================================================
# Unit Conversion Functions
# ==============================================================================

def degToRad(deg):
    # Conversion function for degrees to radians
    rad = deg * (pi / 180.0)    
    return rad

def radToDeg(rad):
    # Conversion function for radians to degrees
    deg = rad * (180.0 / pi)    
    return deg

def parsecToLightYear(psc):
    ly = psc * 3.26163626    
    return ly

def calculateLMST():
        # Calculates Local Mean Siderial Time, accurate in comparison to the old
        # YorkTime program.        
        G = { 2010 : 6.63681, 
              2011 : 6.62089, 
              2012 : 6.60497, 
              2013 : 6.65478, 
              2014 : 6.63886,
              2015 : 6.63681,
              2016 : 6.63681  }        
        #STEPS TO LMST FROM: Observational Astronomy author, D.scott Birney, ed. 2, pg#26
        #step1 //current GMT/UT
        currentTime = time.gmtime()        
        year = currentTime[0]
        month = currentTime[1]
        day = currentTime[2]
        hour = currentTime[3]
        minute = currentTime[4]
        sec = currentTime[5]
        N = currentTime[7]
        #step2 - convert solar interval since 0h UT to sidereal interval
        interval = (hour + (minute / 60.) + (sec / 3600.)) #* 1.00273791 <-- what is this, works better without
        d_interval = (0 + (0 / 60.) + (1.5 / 3600.))
        #step3 - calculate GMST at time of interest
        GMST = 6.63886 + (0.0657098244 * N) + (1.00273791 * interval)
        d_GMST =  (1.00273791 * d_interval)
        # calculate Julian Day number at 0h UT
        L = (year - 2001) / 4
        JDnot = 2451544.5 + 365 * (year - 2000) + N + L        
        # calculate exact Julian Day i.e. including interval since 0h
        JD = JDnot + (interval / 24)        
        #step4 - account for longitude
        if GMST > 24: 
            GMST = GMST - 24            
        ST = GMST + (LONGITUDE / 15.)
        d_ST = d_GMST
        if ST > 24: 
            ST = ST - 24
        elif ST < 0: 
            ST = ST + 24
        hour = int(ST)
        d_hour = d_ST
        minute = int(((ST - hour) * 60))
        d_minute = 60*sqrt(d_ST*d_ST*2)
        sec = int((((ST - hour) * 60 - minute) * 60))
        d_sec = 60*(d_minute/minute)
        LMST = (hour, minute, sec)
        d_LMST = (d_hour, d_minute, d_sec)
        currentLMST = LMST
        return currentLMST


def calculateHourAngle(ra, currentLMST):
        # The calculateHourAngle() function returns the value of the current   
        # Hour Angle, based on the current Local Mean Sidereal Time and the 
        # Right Ascension of the object being observed.                    
        # The function simply reads out the hh/mm/ss for both and converts   
        # to an hour only unit of time.  HA=LMST-RA is calcuated, and the     
        # Hour angle is returned to where it was called from.        
        LMST = currentLMST
        RA = ra
        RAinSecs = 3600*RA[0] + 60*RA[1] + RA[2]
        d_RAinSecs = 0.05
        LMSTinSecs = 3600*LMST[0] + 60*LMST[1] + LMST[2]
        d_LMSTinSecs = 1.5
        HAinSecs = LMSTinSecs - RAinSecs
        d_HAinSecs = sqrt(d_LMSTinSecs*d_LMSTinSecs + d_RAinSecs*d_RAinSecs)
        HAinSecs = int(HAinSecs)
        HA_Hours = HAinSecs/3600
        HA_Mins = (HA_Hours - int(HA_Hours))*60
        HA_Secs = (HA_Mins - int(HA_Mins))*60
        HA_Hours = int(HA_Hours)
        HA_Mins = int(HA_Mins)
        HA_Secs = int(HA_Secs)
        if HA_Hours <= -12:
            HA_Hours = HA_Hours + 24
        if HA_Hours >= 12:
            HA_Hours = HA_Hours - 24
        return HA_Hours, HA_Mins, HA_Secs, d_HAinSecs

def calculateAirmass(currentRA, currentDEC, currentLMST):
    # As a rule, observations should not be done when looking through     
    # an airmass that is >2.  This makes the observations rather           
    # crappy, images are use    less.  This function returns the airmass       
    # given the altitude of the object, so that a tolerance can be set. 
    # The program will exit if the object is at an airmass of >2           

    altitude = calculateAltitude(currentRA, currentDEC, currentLMST)
    airmass = 1. / (cos(degToRad(90.0 - altitude)))
    
    #airmass=Math.acos((90.0-altitude)*DEG_TO_RAD)*   //complex formula
    #     (1.-0.0012*(Math.pow(Math.acos((90.0-altitude)*DEG_TO_RAD),2)-1))
    
    return airmass


def calculateAltitude(currentRA, currentDEC, currentLMST): 
    HA = calculateHourAngle(currentRA, currentLMST)
    
    if HA < -12: HA = HA + 24
    if HA >= 12: HA = HA - 24
    
    HA = HA * 15.0 #this changes HA from HOURS into DEGREES
    DECinDEG = currentDEC[0] + ((currentDEC[1] * 60) + currentDEC[2]) / 3600.

    sin_alt = sin(degToRad(LATITUDE)) * sin(degToRad(DECinDEG)) \
        + cos(degToRad(LATITUDE)) * cos(degToRad(DECinDEG)) * cos(degToRad(HA))
    altitude = radToDeg(asin(sin_alt))
    
    return altitude


def calculateAzimuth(currentRA, currentDEC, altitude, LMST):
    # Compute the azimuth given declination, right ascension, altitude and LMST. 
    LMSTinHOURS = LMST[0] + ((LMST[1] * 60) + LMST[2]) / 3600. #LMST in hours
    RA = currentRA[0] + ((currentRA[1] * 60) + currentRA[2]) / 3600. #RA in hours

    HA = LMSTinHOURS - RA
    if HA < -12: 
        HA = HA + 24
    if HA >= 12: 
        HA = HA - 24
    
    HA = HA * 15.0   # //HA in degrees
    DEC = currentDEC[0] + ((currentDEC[1] * 60) + currentDEC[2]) / 3600. #DEC in degrees
    altitude = degToRad(altitude)
    #altitude = degToRad(calculateAltitude(currentDEC, currentRA, LMST))
    
    cos_az = (sin(degToRad(DEC)) - (sin(altitude) * sin(degToRad(LATITUDE)))) / (cos(altitude) * cos(degToRad(LATITUDE)))
    azimuth = radToDeg(acos(cos_az))
    
    if sin(degToRad(HA)) < 0: 
        azimuth = azimuth + 0
    else: 
        azimuth = 360 - azimuth
    
    return azimuth



def epochJ2k(currentRA, currentDEC):
    # convert back to J2000, needed for stellarium
    
    year = time.localtime()[0]
    month = time.localtime()[1]
        
    if month > 6: 
        year = year + 0.5

    interval = year - 2000.0
    
    m = 46.1244 + (0.000279 * interval)
    n = 20.0431 - (0.000085 * interval)
    
    RAinDEG = currentRA * 15. # RA in degrees
    
    deltaA = (m + n * sin(degToRad(RAinDEG)) * tan(degToRad(currentDEC)))
    deltaD = n * cos(degToRad(RAinDEG))

    RAinHOURS = (RAinDEG - (interval * deltaA) / 3600.) / 15.
    currentDEC = currentDEC - (interval * deltaD) / 3600.
    
    if RAinHOURS < 0.0:
        RAinHOURS = 24.0 + RAinHOURS
    
    return RAinHOURS, currentDEC

def epochConvert(currentRA, currentDEC, userEpoch):
    # The program stars are all hardwired into the program.  The coordinates   
    # are of the J2000.0 epoch (see program summary for list of program stars 
    # and their coordinates).  The epochConvert() routine uses the J2000.0   
    # coordinates and the current year to calculate the current epoch's    
    # coordinates.  This is a useful routine to keep the program independent  
    # from user input.                                                      
    #                                                                        
    # The formulae used for this routine were taken from:                    
    # "Observational Astronomy: 2nd Edition" by Birney, Gonzalez, and Oesper 
    # published: Cambridge University Press, 2006, pg 67
    
    year = time.localtime()[0]
    month = time.localtime()[1]
    
    interval = year - userEpoch
    
    if month > 6: 
        interval = interval + 0.5
    
    m = 46.1244 + (0.000279 * interval)
    n = 20.0431 - (0.000085 * interval)

    RAinDEG = (currentRA[0] + ((currentRA[1] * 60) + currentRA[2]) / 3600.) * 15. # RA in degrees
    DECinDEG = currentDEC[0] + ((currentDEC[1] * 60) + currentDEC[2]) / 3600. # DEC in degrees

    deltaA = (m + n * sin(degToRad(RAinDEG)) * tan(degToRad(DECinDEG)))
    deltaD = n * cos(degToRad(RAinDEG))

    RAinHOURS = (RAinDEG + (interval * deltaA) / 3600.) / 15.
    DECinDEG = DECinDEG + (interval * deltaD) / 3600.

    #NEW RA - i.e. converted to userEpoch   
    hhRA = int(RAinHOURS)
    mmRA = int((RAinHOURS - hhRA) * 60)
    ssRA = (((RAinHOURS - hhRA) * 60) - (int((RAinHOURS - hhRA) * 60))) * 60
    RAreturn = (hhRA, mmRA, ssRA)

    #NEW DEC - i.e. converted to userEpoch
    ddDEC = int(DECinDEG)
    mmDEC = int((DECinDEG - ddDEC) * 60)
    ssDEC = (((DECinDEG - ddDEC) * 60) - (int((DECinDEG - ddDEC) * 60))) * 60
    DECreturn = (ddDEC, mmDEC, ssDEC)
    
    return RAreturn, DECreturn, (userEpoch + interval)


