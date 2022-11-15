# -*- coding: utf-8 -*-


import abc

class Network(abc.ABC):
    
    def __init__(self,theID : str):
        self.__InitializeID(theID)
        
    def __InitializeID(self,theID: str) -> None:
        self.__id=theID
        
    def __InitializeLayerSet(self) -> None:
        pass
    
    def GetID(self) -> str :
        return self.__id
    
#    @abc.abstractmethod
#    def AddLayer(self) -> None:
#        pass
#    
#    @abc.abstractmethod    
#    def HasLayer(self,theID: str)-> bool:
#        return False
#    
#    @abc.abstractmethod
#    def GetLayer(theID: str) -> None:
#        return None 