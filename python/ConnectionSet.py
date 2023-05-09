# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:39:53 2020

@author: MatsWallden
"""
#RESPONSNIBILITIES
#   HOLD THE CONNECTIONS ASSOCIATED WITH ONE NEURON

import uuid

class ConnectionSet(object):
    
    def __init__(self, theID : str):
        self.__InitializeID(theID)
        self.__InitializeConnections()
            
    def __InitializeID(self, theID : str) -> None:
        self.__id=str(uuid.uuid4())
    
    def __InitializeConnections(self) -> None:
        self.__connections=dict()
        
    def SetID(self,theID: str) -> None:
        self.__id=theID
        
    def GetID(self) -> str :
        return self.__id
    
    def AddConnection(self,theConnection: 'Connection' ) -> None:
        if(theConnection.GetID() in self.__connections.keys()):
            pass 
        else:
            self.__connections.update({theConnection.GetID():theConnection})
        
    def GetConnection(self,theConnectionID : str) -> 'Connection' :
        if(theConnectionID in self.__connections):
            return self.__connections[theConnectionID]
        else:
            return None
        
    def GetConnectionIDSet(self) -> list:
        return list(self.__connections.keys())
        