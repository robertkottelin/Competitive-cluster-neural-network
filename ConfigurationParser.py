# -*- coding: utf-8 -*-


class ConfigurationParser(object):
    def __init__(self):
        pass
    
class ConfigurationParser_QPCR_ResultCompiler(ConfigurationParser):
    def __init__(self):
        pass

import os
import xml.etree.ElementTree as ET #FOR THE CONFIGURAITON
from Configuration import Configuration_QPCR_ResultCompiler_SARSCOV2_01
from Sample import ReferenceSample
from Target import Target_QPCR_SARSCOV2_00
from Parameter import Parameter_QPCR_SARSCOV2_00


class ConfigurationParser_QPCR_ResultCompiler_SARSCOV2_00(ConfigurationParser_QPCR_ResultCompiler):
    def __init__(self):
     
        pass
    
    def GetConfig(self,theDirectoryConfig,theConfigFileName):
        theTree=ET.parse(os.path.join(theDirectoryConfig,theConfigFileName))
        
        theDirectoryNode=theTree.findall('DIRECTORY')
        theDirectoryDATA=theDirectoryNode[0].findall("DATA")[0].text
        theDirectoryIO=theDirectoryNode[0].findall("IO")[0].text
        theDirectoryCOMPILER=theDirectoryNode[0].findall("COMPILER")[0].text
        theDirectoryPRINT=theDirectoryNode[0].findall("PRINT")[0].text

        
        theConfig=Configuration_QPCR_ResultCompiler_SARSCOV2_01(theDirectoryPRINT,theDirectoryDATA,theDirectoryIO,theDirectoryCOMPILER)
        
        theControls=theTree.findall("CONTROLS/CONTROL")
                
        for theControlElement in theControls:
            theId=theControlElement.get('id')
            theType=theControlElement.get('type')
            theConfig.AddReferenceSample(ReferenceSample(theId,theType))        

        theTargets=theTree.findall("TARGETS/TARGET")
        
        for theTargetElement in theTargets:
            theId=theTargetElement.get('id')
            theOrigin=theTargetElement.get('origin')
            theConfig.AddTarget(Target_QPCR_SARSCOV2_00(theId,theOrigin))
            
        theParameters=theTree.findall("PARAMETERS/PARAMETER")
        
        for theParameterElement in theParameters:
            theId=theParameterElement.get('id')
            theValue=theParameterElement.get('value')
            theConfig.AddParameter(Parameter_QPCR_SARSCOV2_00(theId,theValue))
        
        return theConfig
    
    
        