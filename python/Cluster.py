# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:23:40 2020

@author: MatsWallden
"""
import numpy
from NeuronSet import NeuronSet

class Cluster(NeuronSet):
    def __init__(self, theID : str):
        super(Cluster,self).__init__(theID)
        self.__InitializeFired()
        
    def __InitializeFired(self):
        self.__fired=False
            
    def GetMaximumActiveNeuron(self):
        
        theMaximumActivity=-1.0
        theMaximumActiveNeuron=None
        
        for theNeuron in self.GetNeuronSet():
            theActivity=theNeuron.GetActivity()
            if(theActivity==theMaximumActivity):
                if(numpy.random.rand()>0.5):
                    theMaximumActivity=theActivity
                    theMaximumActiveNeuron=theNeuron
                else:
                    pass
            elif(theActivity>theMaximumActivity):
                theMaximumActivity=theActivity
                theMaximumActiveNeuron=theNeuron
            else:            
                pass
        
        return theMaximumActiveNeuron
    
    def GetMaximumActivity(self):
        return self.GetMaximumActiveNeuron().GetActivity()
    
    def Fire(self):
        self.GetMaximumActiveNeuron().Fire()
        self.__fired=True
    
    def Reload(self):
        self.__fired=False
        for theNeuron in self.GetNeuronSet():
            theNeuron.Reload()
    
    def GetFired(self):
        return self.__fired
    
    def Update(self,theUpdateStrength :float) -> None:
        self.GetMaximumActiveNeuron().Update(theUpdateStrength)
        
        #reload?
