# -*- coding: utf-8 -*-

#from Directory import Directory
#from RootDirectory import RootDirectory

class Configuration(object):
    def __init__(self):
        pass
    
class Configuration_COMP_ANN(Configuration):
    def __init__(self):
        pass

class Configuration_QPCR_ResultCompiler_SARSCOV2_00(Configuration_QPCR_ResultCompiler):
    
    def __init__(self,theDirectoryPrint,theDirectoryData,theDirectoryIO,theDirectoryCompiler):
        self.SetDirectoryPrint(theDirectoryPrint)
        self.SetDirectoryData(theDirectoryData)
        self.SetDirectoryIO(theDirectoryIO)
        self.SetDirectoryCompiler(theDirectoryCompiler)
        self.SetReferenceSamples()
    
    def SetDirectoryPrint(self,theDirectoryPrint):
        self.__directoryPrint=theDirectoryPrint
        
    def SetDirectoryData(self,theDirectoryData):
        self.__directoryData=theDirectoryData
        
    def SetDirectoryIO(self,theDirectoryIO):
        self.__directoryIO=theDirectoryIO
    
    def SetDirectoryCompiler(self,theDirectoryCompiler):
        self.__directoryCompiler=theDirectoryCompiler
        
    def AddReferenceSample(self,theReferenceSample):
        self.__reference.update({theReferenceSample.GetId():theReferenceSample})

    def GetDirectoryPrint(self):
        return self.__directoryPrint
        
    def GetDirectoryData(self):
        return self.__directoryData
        
    def GetDirectoryIO(self):
        return self.__directoryIO
    
    def GetDirectoryCompiler(self):
        return self.__directoryCompiler    
    
    def GetReferenceSampleById(self,theId):
        if(theId in self.__reference.keys()):
            return self.__reference[theId]
        else:
            return None
        
    def GetReferenceSamplesByType(self,theType):
        
        output=list()
        
        for theReferenceSample in self.__reference.values():
            theType_temp=theReferenceSample.GetType()
            
            if(theType==theType_temp):
                output.append(theReferenceSample)
            else:
                pass
            
        return output
                

class Configuration_Competivitive_ANN_01(Configuration_Competitive_ANN):
    
    def __init__(self,theDirectoryPrint,theDirectoryData,theDirectoryIO,theDirectoryCompiler):
        self.SetDirectoryPrint(theDirectoryPrint)
        self.SetDirectoryData(theDirectoryData)
        self.SetDirectoryIO(theDirectoryIO)
        self.SetDirectoryCompiler(theDirectoryCompiler)
        self.SetTargets()
        self.SetParameters()
        self.SetReferenceSamples()
    
    def SetDirectoryPrint(self,theDirectoryPrint):
        self.__directoryPrint=theDirectoryPrint
        
    def SetDirectoryData(self,theDirectoryData):
        self.__directoryData=theDirectoryData
        
    def SetDirectoryIO(self,theDirectoryIO):
        self.__directoryIO=theDirectoryIO
    
    def SetDirectoryCompiler(self,theDirectoryCompiler):
        self.__directoryCompiler=theDirectoryCompiler
        
    def SetReferenceSamples(self):
        self.__reference=dict()
        
    def SetTargets(self):
        self.__targets=[]
        
    def SetParameters(self):
        self.__parameters=[]
    
    def AddReferenceSample(self,theReferenceSample):
        self.__reference.update({theReferenceSample.GetId():theReferenceSample})
    
    def AddTarget(self,theTarget):
        self.__targets.append(theTarget)
        
    def AddParameter(self,theParameter):
        self.__parameters.append(theParameter) #TODO the type should be anticipated.. 

    def GetDirectoryPrint(self):
        return self.__directoryPrint
        
    def GetDirectoryData(self):
        return self.__directoryData
        
    def GetDirectoryIO(self):
        return self.__directoryIO
    
    def GetDirectoryCompiler(self):
        return self.__directoryCompiler    
    
    def GetReferenceSampleById(self,theId):
        theReferenceSamples=[]
        
        if(theId in self.__reference.keys()):
            theReferenceSamples.append(self.__reference[theId])
        else:
            pass
        
        if('*' in self.__reference.keys()):
            theReferenceSamples.append(self.__reference['*'])
        else:
            pass
        
        if(len(theReferenceSamples)==0):
            theReferenceSamples=None
        else:
            pass
        
        return theReferenceSamples
        
    def GetReferenceSamplesByType(self,theType):
        
        output=list()
        
        for theReferenceSample in self.__reference.values():
            theType_temp=theReferenceSample.GetType()
            
            if(theType==theType_temp):
                output.append(theReferenceSample)
            else:
                pass
            
        return output
    
    def GetReferenceTypes(self):
        
        theReferenceTypes=[]
        for theReferenceSample in list(self.__reference.values()):
            if(not theReferenceSample.GetType() in theReferenceTypes):
                theReferenceTypes.append(theReferenceSample.GetType())
            else:
                pass
                
        return theReferenceTypes
    
    def GetTargets(self):
        return self.__targets
    
    def GetParameters(self):
        return self.__parameters
    
    def GetReferenceType(self,theId):
        theReferenceSamples=self.GetReferenceSampleById(theId)
        
        theReferenceTypes=[]
        
        if(theReferenceSamples is None):
            return None
        else:
            for theReferenceSample in theReferenceSamples:
                theReferenceTypes.append(theReferenceSample.GetType())
                
        return theReferenceTypes
        
    def GetReferenceIDByType(self,theType):
        theReferenceSamples=self.GetReferenceSamplesByType(theType)
        
        theReferenceID = []
        
        for theReferenceSample in theReferenceSamples: 
            
            theReferenceID.append(theReferenceSample.GetId())
        
        return theReferenceID        
        
