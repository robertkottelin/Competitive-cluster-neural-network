# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:52:38 2020

@author: MatsWallden
"""

#from Baptist import *

import abc
import numpy
from Baptist import Baptist
from Baptist import UuidBaptist
from Connection import Connection
from WeightSet import WeightSet
from Weight import Weight

class Neuron(abc.ABC):
    def __init__(self, theID : str):
        self.__InitializeID(theID)
        self.__InitializeActivity()
        self.__fired=False        
    
    def __InitializeID(self,theID : str) -> None:
        self.__id=theID
        
    def __InitializeActivity(self) -> None:
        self.__activity=None
        
      
    def SetActivity(self, theActivity: float) -> None:
        self.__activity=theActivity
        
    def GetID(self):
        return self.__id
    
    @abc.abstractmethod
    def GetActivity(self):
        pass
    
    def GetFired(self):
        return self.__fired

    def Fire(self):
        self.__fired=True
    
    @abc.abstractmethod        
    def Reload(self):
        self.__fired=False
        self.Reset()
    
    @abc.abstractmethod
    def Reset(self):
        self.__activity=None
        
class InputNeuron(Neuron):
    def __init__(self, theID : str):
        super(InputNeuron,self).__init__(theID)
        super(InputNeuron,self).Fire()
        self.__InitializeActivity()
        

    def __InitializeActivity(self) -> None :
        self.__activity=None
    
    def SetActivity(self,theActivity: float)-> None:
        self.__activity=theActivity
        
    def GetActivity(self):
        return self.__activity

    def Reload(self):
        pass
    
    def Reset(self):
        pass
    
#import numpy
#from Weight import Weight
#from WeightSet import WeightSet

class InhibitoryNeuron(Neuron):
    def __init__(self, theID : str ):
        super(InhibitoryNeuron,self).__init__(theID)
        self.__InitializeConnection()
        self.__connectedID2WeightID={}
        #self.__InitializeConnectedID2WeightID()
        self.__InitializeWeightSet()

    
    def __InitializeWeightSet(self):
        self.__weightSet=WeightSet(theID=UuidBaptist.Baptize())
    
    def __InitializeConnectedID2WeightID(self):
        self.__connectedID2WeightID=dict()
        
    def __PurgeConnectedID2WeightID(self):
        self.__InitializeConnectedID2WeightID()
    
    def Connect(self, theNeuron : 'Neuron')-> None:
        if(not theNeuron.GetID() in self.__connection.GetConnectedIDSet()):
            self.__connection.Connect(theNeuron)
        else:
            pass

    def GetActivity(self):
    
        theActivity=super(InhibitoryNeuron,self).GetActivity()
        
        if(theActivity is not None):
           # print("10011")
            return theActivity
        else:            
            pass
        
        theActivity=0.0
        
        theConnectedIDSet=self.__connection.GetConnectedIDSet()
        
        for theConnectedID in theConnectedIDSet:
            theConnectedActivity=self.GetConnected(theConnectedID).GetActivity()
            
            theWeight=self.GetWeight(theConnectedID=theConnectedID)
            
            theActivity+=theConnectedActivity*theWeight.GetValue()
        
        super(InhibitoryNeuron,self).SetActivity(theActivity)
        
        return theActivity
    
    def GetConnected(self,theConnectedID : str ) -> None :
        if(self.IsConnected(theConnectedID =theConnectedID)):
            return self.__connection.GetConnected(theConnectedID) 
        else:
            return None
    
    def IsConnected(self,theConnectedID : str ):
        return self.__connection.IsConnected(theID=theConnectedID)
    
    def GetWeight(self, theConnectedID: str) -> None:
        if(self.__HasConnectedID2WeightID(theConnectedID = theConnectedID)):
            theWeight=self.__weightSet.GetWeight(theID=self.__GetConnectedID2WeightID(theConnectedID=theConnectedID))
            return theWeight
        else:
            return None
    
    def InitializeWeightSet(self) -> None:
        theNumberConnections=self.__connection.GetNumberConnection()
        theConnectedIDSet=self.__connection.GetConnectedIDSet()
                        
        self.__PurgeConnectedID2WeightID()
        
        self.__weightSet.Purge()
        
        theValues=numpy.random.random(size=theNumberConnections)
        
        theValues=theValues/theValues.sum()
        
        for theIndex in range(len(theValues)):
            theWeight=Weight(theID=UuidBaptist.Baptize())
            theWeight.SetValue(theValue=theValues[theIndex])
            self.__weightSet.Add(theWeight=theWeight)
            self.__SetConnectedID2WeightID(theConnectedID=theConnectedIDSet[theIndex],theWeightID=theWeight.GetID())
            
    def NormalizeWeightSet(self):
        theConnectedIDSet=self.__connection.GetConnectedIDSet()
        theValueSet=dict.fromkeys(theConnectedIDSet)
        theSum=0.0
        
        for theConnectedID in theConnectedIDSet:
            theValueSet[theConnectedID]=self.GetWeight(theConnectedID=theConnectedID).GetValue()
            theSum+=theValueSet[theConnectedID]
        
        for theConnectedID in theConnectedIDSet:
            self.GetWeight(theConnectedID=theConnectedID).SetValue(theValueSet[theConnectedID]/theSum)
    
    def __InitializeConnection(self) -> None :
        self.__connection=Connection(theID=UuidBaptist.Baptize())
    
    def Reload(self) -> None:
        super(InhibitoryNeuron,self).Reload()
        
    def Reset(self) -> None:
        super(InhibitoryNeuron,self).Reset()

    def __HasConnectedID2WeightID(self,theConnectedID : str )->None:
        if(theConnectedID in self.__connectedID2WeightID.keys()):
            return True
        else:
            return False            
    
    def __GetConnectedID2WeightID(self,theConnectedID : str) -> None:
        if(theConnectedID not in self.__connectedID2WeightID.keys()):
            raise("theConnection does not exist")
        else:
            return self.__connectedID2WeightID[theConnectedID]
        
    def __SetConnectedID2WeightID(self,theConnectedID: str, theWeightID : str )-> None:
        if(self.__HasConnectedID2WeightID(theConnectedID)):
            raise(" weight already exists") 
        else:
            self.__connectedID2WeightID.update({theConnectedID:theWeightID})

    def Update(self,theUpdateStrength : float ) -> None:
        theTotalConnectedActivity=0
        
        theConnectedIDSet=self.__connection.GetConnectedIDSet()
        
        theConnectedActivity=dict.fromkeys(theConnectedIDSet)
        
        theWeightSum=0.0
    
        theWeightSet=dict.fromkeys(theConnectedIDSet)
        
        for theConnectedID in theConnectedIDSet:

            #theConnectedActivity[theConnectedID]=self.GetConnected(theConnectedID).GetActivity() #cik
             
            theConnectedActivity[theConnectedID]=self.GetConnected(theConnectedID).GetActivity()*self.GetWeight(theConnectedID=theConnectedID).GetValue() #cik
             
            theTotalConnectedActivity+=theConnectedActivity[theConnectedID]

        for theConnectedID in theConnectedActivity.keys():
            
            theWeight=self.GetWeight(theConnectedID=theConnectedID)
            
            theUpdateWeight=theUpdateStrength*(theConnectedActivity[theConnectedID]/theTotalConnectedActivity-theWeight.GetValue())

            theWeight.Update(theUpdate=theUpdateWeight)
            
            theWeightSum+=theWeight.GetValue()
            
            theWeightSet[theConnectedID]=theWeight
 
        for theConnectedID in theConnectedIDSet:
            
            theWeightSet[theConnectedID].SetValue(theValue=theWeightSet[theConnectedID].GetValue()/theWeightSum)