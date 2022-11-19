# -*- coding: utf-8 -*-

from Cluster import Cluster
import abc

class ClusterSet(abc.ABC):
    
    def __init__(self,theID : str):
        self.__InitializeID(theID)   
        self.__InitializeClusterSet()

    def __InitializeID(self,theID : str)-> None:
        self.__id=theID

    def __InitializeClusterSet(self) -> str:
        self.__clusterSet=dict()
        
    def GetID(self):
        return self.__id

    def HasCluster(self, theID : str ) -> bool:
        if(theID in self.__clusterSet.keys()):
            return True
        else:
            return False
        
    def GetClusterIDSet(self):
        return list(self.__clusterSet.keys())

    def AddCluster(self, theCluster : 'Cluster' ) -> None:
        if(not theCluster.GetID() in self.__clusterSet.keys() ):
            self.__clusterSet.update({theCluster.GetID(): theCluster})
        else:
            pass
        
    def RemoveCluster(self, theID : str) -> None:
        if(self.HasCluster(theID)):
            del self.__clusterSet[theID]
        else:
            pass
        
    def GetCluster(self,theID :str ) -> 'Cluster':
        if(self.HasCluster(theID)):
            return self.__clusterSet[theID]
        else:
            return None
        
    def GetMaximumActiveCluster(self):
        
        theMaximumActiveCluster=None
        
        theMaximumActivity=-1.0
        
        for theCluster in self.__clusterSet.values():
            theActivity=theCluster.GetMaximumActivity()
            if(theActivity>theMaximumActivity):
                theMaximumActivity=theActivity
                theMaximumActiveCluster=theCluster
            else:
                pass  
#        print(theMaximumActiveCluster.GetMaximumActiveNeuron().GetID() + " "+ str(theMaximumActiveCluster.GetMaximumActiveNeuron().GetActivity()) )  //update
        return theMaximumActiveCluster
    
    def Fire(self)-> None:
        for theCluster in self.__clusterSet.values():
            theCluster.Fire()
    
    def Reload(self) -> None:
        for theCluster in self.__clusterSet.values():
            theCluster.Reload()
    
    def Update(self,theUpdateStrength : float) -> None:
        self.GetMaximumActiveCluster().Update(theUpdateStrength)
        
