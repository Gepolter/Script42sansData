'''
Created on 26.02.2022

@author: Dominik
'''

import numpy as np
import pandas as pd
from pathlib import Path
from asyncio import streams
import scipy
from scipy.integrate._quadpack_py import quad
import os
from scipy import integrate



if __name__ == '__main__':  
   
    constant = 806.6
    
    #directory of intensity ZOE: FILEPATH!!!!!
    intensityFileStr = r"C:\Users\Dominik\Documents\RaUpPyr_change_bITO_SiN_MgF_ges\RaUpPyr_change_bITO_SiN_MgF_ges\EQE intensity\Intensity.csv"
    dataFrameIntensity = pd.read_csv(intensityFileStr, sep = ";")
    dataFrameIntensity = dataFrameIntensity.reset_index(drop=True)
    
    dataFrameIntensity.drop_duplicates() 
    
    
    #Repository structure TPC -> xxx loop over all 
    #                                           xxxxxxx loop over all
    #                                                                raqxxx -> EQE                                   
    
    #directory of datasets ZOE: DIRECTORY PAHT!!!
    directoryInStr = r"C:\Users\Dominik\Documents\RaUpPyr_change_bITO_SiN_MgF_ges\RaUpPyr_change_bITO_SiN_MgF_ges\EQE"
    
    pathlist = Path(directoryInStr).glob('**/*.dat')
    
    def func(x):
        return x**2
    
    #loop over paths in EQE directory
    for path in pathlist:
        
        pathInStr = str(path)
        print(pathInStr)
        
        dataframe = pd.read_csv(pathInStr, sep = " ")#, index_col = None)
        dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
        """
        new_header = dataframe.iloc[0] #grab the first row for the header
        dataframe = dataframe[1:] #take the data less the header row
        dataframe.columns = new_header #set the header row as the df header
        """
        #dataframe.rename( columns={'Unnamed: 0':'new column name'}, inplace=True )
        
        #adding column intensity

        dataframe = pd.concat([dataframe, dataFrameIntensity], axis = 1)
        
        
        #adding calculation
        dataframe["Wavelength_Absorbed_wafer_Intensity_constant"] = dataframe.Wavelength * dataframe.Absorbed_wafer * constant * dataframe.intensity
        
        #integrating
        
        #dataframe["Integral"] = integrate.simpson(dataframe.Wavelength_Absorbed_wafer_Intensity_constant, dataframe.Wavelength)
        
        dataframe["Integral"] = integrate.simpson(dataframe.Wavelength, dataframe.Wavelength_Absorbed_wafer_Intensity_constant)
        
        #quad(dataframe.Wavelength_Absorbed_wafer_Intensity_constant, 0, 3)
        
        #empty/previous results directory ZOE: DIRECTORY PATH!
        dataframe.to_csv(r"C:\Users\Dominik\Documents\RaUpPyr_change_bITO_SiN_MgF_ges\RaUpPyr_change_bITO_SiN_MgF_ges\EQE new\i" + str(os.path.basename(pathInStr)), sep = ";", index = False)
        
        
        
        
        
    