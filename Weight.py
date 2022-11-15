# -*- coding: utf-8 -*-

import numpy

class Weight(object):
    def __init__(self, theID : str):
        self.__InitializeID(theID)
        self.__InitializeValue()        
    
    def __InitializeID(self, theID: str)-> None:
        self.__id=theID
    
    def __InitializeValue(self) -> None:
        self.__value=numpy.nan
        
    def GetID(self) -> str :
        return self.__id
    
    def SetValue(self,theValue: float )-> None :
        if(theValue <= 1.0):
            self.__value=theValue
        else:
            self.__value=1.0
    
    def GetValue(self) -> float :
        return self.__value
    
    def Update(self,theUpdate : float) -> None:
        self.SetValue(self.GetValue()+theUpdate)
        