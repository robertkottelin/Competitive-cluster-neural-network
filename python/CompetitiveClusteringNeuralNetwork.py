# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 17:52:35 2020

@author: MatsWallden
"""

#Responsibility

from Network import Network
from InputLayer import InputLayer
from InhibitoryLayer import InhibitoryLayer

class CompetitiveClusteringNeuralNetwork(Network):    
    
    def __init__(self, theID: str ):
        super(CompetitiveClusteringNeuralNetwork,self).__init__(theID)       
        self.__InitializeInputLayerSet()
        self.__InitializeInhibitoryLayerSet()
        self.__InitializeOutputLayerID()
    
    def __InitializeInputLayerSet(self) -> None :
        self.__inputLayerSet=dict()
        
    def __InitializeInhibitoryLayerSet(self) -> None:
        self.__inhibitoryLayerSet=dict()
    
    def __InitializeOutputLayerID(self) -> None:
        self.__outpuLayerID=None    
    
    def HasInhibitoryLayer(self,theID :str ) -> bool:
        if(theID in self.__inhibitoryLayerSet.keys()):
            return True
        else:
            return False
        
    def HasInputLayer(self, theID : str ):
        if(theID in self.__inputLayerSet.keys()):
            return True
        else:
            return False
    
    def AddInputLayer(self,theInputLayer : 'InputLayer') -> None: 
        if(not self.HasInputLayer(theInputLayer.GetID())):
              self.__inputLayerSet.update({theInputLayer.GetID() : theInputLayer })
        else:
            pass
        
    def AddInhibitoryLayer(self,theInhibitoryLayer : 'InhibitoryLayer') -> None:
        if(not self.HasInhibitoryLayer(theInhibitoryLayer.GetID())):
            self.__inhibitoryLayerSet.update({theInhibitoryLayer.GetID(): theInhibitoryLayer})
        else:
            pass
    
    def GetOutputLayerID(self):
        return self.__outputLayerID
    
    def GetInhibitoryLayer(self, theID : str )-> 'InhibitoryLayer':
        if(self.HasInhibitoryLayer(theID)):
            return self.__inhibitoryLayerSet[theID]
        else:
            return None
    
    def GetInputLayer(self, theID : str )-> 'InputLayer':
        if(self.HasInputLayer(theID)):
            return self.__inputLayerSet[theID]
        else:
            return None
        
    def SetOutputLayer(self,theOutputLayerID : str )-> None:
        self.__outputLayerID=theOutputLayerID
                        
    def Load(self,theInputActivitySet : dict ) -> None: 
        #Get a list of neurons in the set
        for theInputLayerID in self.__inputLayerSet.keys():
            
            theNeuronIDSet=self.__inputLayerSet[theInputLayerID].GetNeuronIDSet()
            
            for theNeuronID in theInputActivitySet.keys():
                
                if(theNeuronID in theNeuronIDSet):
                    self.__inputLayerSet[theInputLayerID].SetActivity(theID=theNeuronID,theActivity=theInputActivitySet[theNeuronID])
                else:
                    pass
                
        self.Reload(theID=None)

    def Reload(self,theID=None) -> None:
        if(theID is None):
            for theInhibitoryLayerID in self.__inhibitoryLayerSet.keys():
                self.GetInhibitoryLayer(theID=theInhibitoryLayerID).Reload()
        elif(theID in self.__inhibitoryLayerSet.keys()):
            self.GetInhibitoryLayer(theID=theID).Reload()
        else:
            pass

    def  Update(self,theUpdateStrength: float):
        
        self.Fire()
        
        for theInhibitoryLayerID in self.__inhibitoryLayerSet.keys():
            self.GetInhibitoryLayer(theID=theInhibitoryLayerID).Update(theUpdateStrength=theUpdateStrength)
        
    def Fire(self):
        for theInhibitoryLayerID in self.__inhibitoryLayerSet.keys():
            self.GetInhibitoryLayer(theID=theInhibitoryLayerID).Fire()
       
    def GetActivity(self,theID=None) -> dict :
        
        if(theID is None or theID == self.GetOutputLayerID):
            # select all nodes in the output layer (an inibitory layer)
#            print(theID)
            theID = self.GetOutputLayerID()
            
            theClusterIDSet=self.__inhibitoryLayerSet[theID].GetClusterIDSet()
            
            theActivity=dict.fromkeys(theClusterIDSet)
            
            for theClusterID in theClusterIDSet:
                theActivity[theClusterID]=self.__inhibitoryLayerSet[theID].GetCluster(theID=theClusterID).GetMaximumActivity()
            
            return theActivity
        else:
            pass
        
        if(theID in self.__inputLayerSet.keys()):
            # select an input layer
            theActivity=dict.fromkeys(self.GetInputLayer(theID=theID).GetNeuronIDSet())
            
            for theNeuronID in theActivity.keys():
                theActivity[theNeuronID]=self.GetInputLayer(theID=theID).GetActivity(theID=theNeuronID)
            
            return theActivity
        
        else:
            pass
        
        
        for theInhibitoryLayerID in self.__inhibitoryLayerSet.keys():
            if(self.__inhibitoryLayerSet[theInhibitoryLayerID].HasCluster(theID=theID)):
                #select a cluster, returns the maximum activity of the cluster
                return self.__inhibitoryLayerSet[theInhibitoryLayerID].GetCluster(theID=theID).GetMaximumActivity()
            else:
                pass
        
        for theInputLayerID in self.__inputLayerSet.keys():
            if(theID in self.__inputLayerSet[theInputLayerID].GetNeuronIDSet()):
                # selected a input neuron
                return self.__inputLayerSet[theInputLayerID].GetActivity(theID=theID)
            else:
                pass
            
        #selected an inhibitory neuron
        for theInhibitoryLayerID in self.__inhibitoryLayerSet.keys():
            for theClusterID in self.__inhibitoryLayerSet[theInhibitoryLayerID].GetClusterIDSet():                
                if(self.__inhibitoryLayerSet[theInhibitoryLayerID].GetCluster(theClusterID).HasNeuron(theID=theID)):
                    return self.__inhibitoryLayerSet[theInhibitoryLayerID].GetNeuron(theID=theID).GetActivity()
                else:
                    pass
                
        return None        
        


