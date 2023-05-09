# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 12:52:58 2021

@author: rober
"""
import pandas as pd
import numpy
import os



path='C:/Users/rober/COMPANN/Infiles/'

filelist = os.listdir(path)
os.chdir('/Users/rober/COMPANN/Infiles/')

 
# open_file = open(file,'r')
# read_file = open_file.read()
# print(read_file)
rawdata = pd.read_fwf(filelist, header=418, sep="\t")
rawdata=rawdata[:17280]
# print(rawdata)

#Define columns and convert to float
split_data = rawdata["Well\tWell Position\tCycle\tx1-m1\tx2-m2\tx3-m3\tx4-m4\tx5-m5"].str.split("\t")
data = split_data.to_list()
names = ["Well", "Well_Position", "Cycle", "FAM", "x2", "x3", "ROX", "x5"]

df = pd.DataFrame(data, columns=names)
df = df.replace(',','', regex=True)

df["Well"] = df["Well"].astype(float)
df["Cycle"] = df["Cycle"].astype(float)
df["FAM"] = df["FAM"].astype(float) #channel
df["x2"] = df["x2"].astype(float) #channel
df["x3"] = df["x3"].astype(float) #channel
df["ROX"] = df["ROX"].astype(float) #channel
df["x5"] = df["x5"].astype(float) #channel

rawdata=df

# print(rawdata)
    
    
    
well=1
    
while well < 385:
    
    is_well = rawdata["Well"]==well
    this_well = rawdata[is_well]
    
    #FAM
    FAM = this_well["FAM"]
    FAM_norm=(FAM-FAM.min())/(FAM.max()-FAM.min())
    FAM_vector=FAM_norm.to_numpy()
    
    
    #x2
    x2 = this_well["x2"]
    x2_norm=(x2-x2.min())/(x2.max()-x2.min())
    x2_vector=x2_norm.to_numpy()
    
    #x3
    x3 = this_well["x3"]
    x3_norm=(x3-x3.min())/(x3.max()-x3.min())
    x3_vector=x3_norm.to_numpy()
    
    #ROX
    ROX = this_well["ROX"]
    ROX_norm=(ROX-ROX.min())/(ROX.max()-ROX.min())
    ROX_vector=ROX_norm.to_numpy()
    
    #x5
    x5 = this_well["x5"]
    x5_norm=(x5-x5.min())/(x5.max()-x5.min())
    x5_vector=x5_norm.to_numpy()
    
    if well == 1:
        
        vectors = {'FAM_vector': [FAM_vector],
            'x2_vector': [x2_vector],
            "x3_vector": [x3_vector],
            "ROX_vector": [ROX_vector],
            "x5_vector": [x5_vector]
            }
        vectors = pd.DataFrame(vectors, columns = ["FAM_vector", 
                                                    "x2_vector", 
                                                    "x3_vector", 
                                                    "ROX_vector", 
                                                    "x5_vector"])
    else:
        # vectors.loc[len(vectors.index)] = ["FAM", x2_vector, x3_vector, ROX_vector, x5_vector]
        
        df2 = {'FAM_vector': FAM_vector, 
                'x2_vector': x2_vector, 
                'x3_vector': x3_vector, 
                "ROX_vector": ROX_vector, 
                "x5_vector": x5_vector} 
        vectors = vectors.append(df2, ignore_index = True)
        
        # FAM_vector.append(vectors, ignore_index=True)
        # x2_vector.append(vectors, ignore_index=True)
        # x3_vector.append(vectors, ignore_index=True)
        # ROX_vector.append(vectors, ignore_index=True)
        # x5_vector.append(vectors, ignore_index=True)
    
     
    well+=1
    print(vectors)

   


# vectorfile=vectors
# vectorfile.to_csv(r'C:\Users\rober\COMPANN\Outfiles\vectors.txt')

# def savevectors():
#     #Save vectors as file
#     vectorfile=getvectors()
#     vectorfile.to_csv(r'C:\Users\rober\COMPANN\Outfiles')
#     return vectorfile