# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:49:49 2020

@author: MatsWallden
"""
import abc

class Baptist(abc.ABC):
    
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def Baptize(self):
        pass
    
import uuid


class UuidBaptist(Baptist):
    
    def __init__(self):
        super(UuidBaptist,self).__init__()
        self.__InitializeID()
        
    def __InitializeID(self) -> None:
        self.__id=self.Baptize()
    
    @staticmethod
    def Baptize() -> str:
        return str(uuid.uuid4())
        