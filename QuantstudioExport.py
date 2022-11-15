# -*- coding: utf-8 -*-


import pandas as pd
import numpy

def readdata():
    #Read Quantstudio export txt file and slice out RawData
    Quant = pd.read_fwf('C:/Users//COMPANN/Infiles', 
                     header=418,
                     sep="\t") #TODO loop through multiple files
    #Select RAWDATA
    rawdata = Quant[:17280]
    
    #Define columns and convert to float
    split_data = rawdata["Well\tWell Position\tCycle\tx1-m1\tx2-m2\tx3-m3\tx4-m4\tx5-m5"].str.split("\t")
    data = split_data.to_list()
    names = ["Well", "Well_Position", "Cycle", "FAM", "x2", "x3", "ROX", "x5"]
    df = pd.DataFrame(data, columns=names)
    df = df.replace(',','', regex=True)
    
    df["Well"] = df["Well"].astype(float)
    df["Cycle"] = df["Cycle"].astype(float)
    df["FAM"] = df["FAM"].astype(float)
    df["x2"] = df["x2"].astype(float)
    df["x3"] = df["x3"].astype(float)
    df["ROX"] = df["ROX"].astype(float)
    df["x5"] = df["x5"].astype(float)
    return df

rawdata=readdata()


def getvector(well, channel):
    #Choose which well
    #Choose ROX or FAM as channel
    is_well = rawdata["Well"]==well
    which_well = rawdata[is_well]

    if channel=="ROX": 
        which_channel = which_well["ROX"]
        which_channel_norm=(which_channel-which_channel.min())/(which_channel.max()-which_channel.min())
        vector=which_channel_norm.to_numpy()

    else: 
        which_channel = which_well["FAM"]
        which_channel_norm=(which_channel-which_channel.min())/(which_channel.max()-which_channel.min())
        vector=which_channel_norm.to_numpy()

    return vector

#TODO loop through wells and create subsequent vectors



