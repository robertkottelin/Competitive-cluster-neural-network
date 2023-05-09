# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:35:21 2020

@author: MatsWallden
"""

import abc

class LayerSet(abc.ABC):
    
    def __init__(self,theID : str):
        self.__InitializeID(theID)
        
    def __InitializeID(self,theID: str) -> None:
        self.__id=theID
        
    def __InitializeLayerSet(self) -> None:
        pass
    
    def GetID(self) -> str :
        return self.__id
    
    @abc.abstractmethod
    def AddLayer(self) -> None:
        pass
    
    @abc.abstractmethod    
    def HasLayer(self,theID: str)-> bool:
        return False
    
    @abc.abstractmethod
    def GetLayer(theID: str) -> None:
        return None        