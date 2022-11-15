# -*- coding: utf-8 -*-

import abc
from Neuron import Neuron

class NeuronSet(abc.ABC):
    
    def __init__(self,theID : str):
        self.__InitializeID(theID)
        self.__InitializeNeuronSet()
        
    def __InitializeID(self, theID : str ) -> None:
        self.__id=theID
        
    def __InitializeNeuronSet(self) -> None:
        self.__neuronSet=dict()
    
    def GetID(self) -> str:
        return self.__id
    
    def AddNeuron(self,theNeuron: 'Neuron' ) -> None:
        if(not self.HasNeuron(theNeuron.GetID())):
            self.__neuronSet.update({theNeuron.GetID(): theNeuron})
        else:
            pass
        
    def HasNeuron(self, theID : str ) -> bool:
        if(theID in self.__neuronSet.keys()):
            return True
        else:
            return False
    
    def GetNeuron(self,theID : str) -> 'Neuron':
        if(self.HasNeuron(theID)):
            return self.__neuronSet[theID]
        else:
            pass
        
    def GetNeuronSet(self):
        return list(self.__neuronSet.values())
    
    def GetNeuronIDSet(self):
        return list(self.__neuronSet.keys())
    
    def __eq__(self,theOtherNeuronSet : 'NeuronSet') -> bool:
        if(self.GetID() == theOtherNeuronSet.GetID()):
            return True
        else:
            return False
    
    