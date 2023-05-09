# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:47:57 2020

@author: MatsWallden
"""

class Connection(object): 
    def __init__(self, theID : str ):
        self.__InitializeID(theID)
        self.__InitializeSet()

    def __InitializeID(self, theID : str ) -> None:
        self.__SetID(theID)
        
    def __InitializeSet(self) -> None:
        self.__set=dict()

    def __SetID(self,theID: str )-> None:
        self.__id=theID        
        
    def GetID(self) -> str:
        return self.__id
    
    def Connect(self,theNeuron : 'Neuron' ) -> None:
        if(not self.IsConnected(theNeuron.GetID())):
            self.__set.update({theNeuron.GetID():theNeuron}) 
        else:
            pass
        
    def Disconnect(self,theID : str) -> None:
        if(self.IsConnected(theID)):
            del self.__set[theID]
        else:
            pass
    
    def GetConnectedIDSet(self):
        return list(self.__set.keys())
    
    def GetNumberConnection(self):
        return len(self.__set)
    
    def GetConnectedSet(self):
        return list(self.__set.values())

    def GetConnected(self,theID):
        if(self.IsConnected(theID)):
            return self.__set[theID]
        else:
            return None
    
    def IsConnected(self,theID: str )-> bool:
        if(theID in self.__set.keys()):
            return True
        else:
            return False

