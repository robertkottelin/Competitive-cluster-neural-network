# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 07:12:49 2020

@author: MatsWallden
"""

from NeuronSet import NeuronSet
import abc

class Layer(abc.ABC):
    def __init__(self, theID : str ):
        self.__InitializeID(theID)
        
    def __InitializeID(self, theID : str) -> None:
        self.__id=theID
            
    def __InitializeNeurons(self):
        self.__neurons=dict()
        
    def __HasNeuron(self,theNeuronID : str )-> bool:
        return theNeuronID in self.__neurons.keys()
    
    def ___AddNeuron(self,theNeuron : 'Neuron' ) -> None:
        if(not self.__HasNeuron(theNeuron.GetID())):
            self.__neurons.update({theNeuron.GetID():theNeuron})
        else:
            pass

    def GetNeuron(self, theID : str )-> 'Neuron':
        if(not theID in self.__neurons.keys()):
            return None
        else:
            return self.__neurons[theID]

