# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 19:59:14 2020

@author: MatsWallden
"""

from ClusterSet import ClusterSet

class InhibitoryLayer(ClusterSet):
    def __init__(self, theID : str):
        super(InhibitoryLayer,self).__init__(theID)
        
    def AddNeuron(self,theClusterID : str, theNeuron : 'Neuron'):
        if(self.HasCluster(theID=theClusterID)):
            self.GetCluster(theID=theClusterID).AddNeuron(theNeuron=theNeuron)
        else:
            pass
	
    def GetNeuron(self,theID: str ) -> 'Neuron':        
        for theClusterID in self.GetClusterIDSet():
            if(not self.GetCluster(theID=theClusterID).HasNeuron(theID=theID)):
                continue
            else:
                #TODO. deal with that this will return the first instance only
                return self.GetCluster(theID=theClusterID).GetNeuron(theID=theID)
            
    def GetActivity(self, theID : str ) -> float:
        
        theNeuron=self.GetNeuron(theID=theID)
        
        if(theNeuron is None):
            return theNeuron.GetActivity()        
        else:
            return None
        
