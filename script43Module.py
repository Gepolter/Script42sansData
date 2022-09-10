'''
Created on 26.02.2022

@author: Dominik
'''

import pandas as pd
from pathlib import Path
import os
from scipy import integrate
import re
import natsort
from natsort.natsort import natsort_keygen
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory



if __name__ == '__main__':  
   
    #functions for humans sort
    #atoi str -> int
    pd.set_option("display.float_format", "{:e}".format)
    pd.set_option("display.precision", 14)
    
    def sort_nicely(l):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('(\d)', key) ]
        l.sort_values( key=alphanum_key )
        
    constant = 806.6
    
    #select path via filechooser 
    filepath = askdirectory()
    
    print(filepath)
    
    #pathlist of all data inside current EQE repo
    pathlistEQE = Path(filepath).glob('**/*.dat')
    
    for path in pathlistEQE:
        
        pathinStrEQEMeasurements = str(path)
        print (pathinStrEQEMeasurements)
        #instantiate dataframe -> stores data from .dat files to work with
        dataframeEQECalc = pd.read_csv(pathinStrEQEMeasurements, " ", decimal = ".", engine = "python")
        #locate unnamed(empty) columns and deletethem
        dataframeEQECalc = dataframeEQECalc.loc[:, ~dataframeEQECalc.columns.str.contains('^Unnamed')]
        
        #NOTadding column intensity
        #dataframeEQECalc = pd.concat([dataframeEQECalc, dataframeIntensity], axis = 1)
        
        #adding calculation
        dataframeEQECalc["Escaped"]\
        = dataframeEQECalc.Escaped + 0.0316 * (1 - dataframeEQECalc.Escaped)
        
        columnstring = r"A(encapsulant/wafer).layer2"
        
        dataframeEQECalc["Absorbed_wafer"]\
        = dataframeEQECalc.Absorbed_wafer * (1-0.0361) + dataframeEQECalc["A(encapsulant/wafer).layer2"] * 0.3
        
        
        testnumber = dataframeEQECalc.dtypes
        dataframeEQECalc.round(decimals = 14)
        
        
        newFileStr = filepath + r"/new " + str(os.path.basename(str(path)))
        dataframeEQECalc.to_csv(newFileStr, sep = " ", index = False, float_format = "{:.14e}".format)
        
        
      
