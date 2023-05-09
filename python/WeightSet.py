# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 22:51:53 2020

@author: MatsWallden
"""
#from Weight import Weight

# RESPONSIBILITIES: 
#   HOLD WEIGHTS ASSOCIATED WITH ONE NEURON

class WeightSet(object):
    def __init__(self,theID : str):
        self.__InitializeID(theID)
        self.__InitializeWeights()
    
    def __InitializeID(self, theID : str) -> None:
        self.__id=theID
    
    def __InitializeWeights(self)-> None:
        self.__weightSet=dict()
    
    def GetID(self) -> str :
        return self.__id
    
    def Add(self,theWeight):
        self.__weightSet.update({theWeight.GetID():theWeight})
    
    def GetWeight(self,theID):
        return self.__weightSet[theID]
        
    def HasWeight(self,theID : str)-> bool:
        if(theID in self.__weightSet.keys()):
            return True
        else:
            return False

    def Remove(self,theID : str)->None:
        if(self.HasWeight(theID)):
            del self.__weightSet[theID]
        else:
            pass
        
    def Purge(self) -> None:
        
        keepGoing=True
                        
        while keepGoing:
            theIDSet=list(self.__weightSet.keys())
            if(len(theIDSet)==0):
                keepGoing=False
                continue
            else:
                self.Remove(theIDSet[0])
    
        