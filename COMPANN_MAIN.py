


#%% IMPORTS

import sys

sys.path.append("C:/Users//PROJECTS/COMPANN")

import uuid
from Connection import Connection
from Baptist import Baptist
from Baptist import UuidBaptist
from Weight import Weight
from WeightSet import WeightSet
from Neuron import Neuron
from Neuron import InputNeuron
from Neuron import InhibitoryNeuron
from NeuronSet import NeuronSet
from InputLayer import InputLayer
from InhibitoryLayer import InhibitoryLayer
from Cluster import Cluster
from ClusterSet import ClusterSet
from Network import Network
from CompetitiveClusteringNeuralNetwork import CompetitiveClusteringNeuralNetwork 
#import QuantstudioExport
import numpy
import pandas



#%% USED FOR TRAINING EXAMPLE


def GetDataNoiseUniform() -> float:
    return numpy.random.rand()

def GetDataFirstOrderPolynomialWithNoise(theIndex:int,theIndexMax: int):
    theData=theIndex/theIndexMax + numpy.random.exponential(scale=0.01)
    if(theData>1.0):
        theData=1.0
    return theData

def GetDataFirstOrderPolynomial(theIndex:int,theIndexMax: int):
    theData=theIndex/theIndexMax
    return theData

def GetDataFirstOrderPolynomialReverse(theIndex:int,theIndexMax: int):
    theData=1-theIndex/theIndexMax
    return theData
    
#%% PARAMETERS 

theNumberNeuronsPerInputLayer=100
theNumberNeuronsPerInhibitoryCluster01=10
theNumberNeuronsPerInhibitoryCluster02=10
theNumberClustersPerInhibitoryLayer01=10
theNumberClustersPerInhibitoryLayer02=10
theUpdateStrength=0.01


#%% CONSTRUCTION 
theInputLayer=InputLayer(UuidBaptist.Baptize())

theInputNeuronIDSet=[]

for theIndex in range(theNumberNeuronsPerInputLayer):
    theInputNeuron=InputNeuron(theID=UuidBaptist.Baptize()) #TODO naming here Channel01Cycle001
    theInputNeuron.SetActivity(numpy.random.rand())
    theInputNeuronIDSet.append(theInputNeuron.GetID())
    theInputLayer.AddNeuron(theNeuron=theInputNeuron)
    
theClusterIDSet01=[]
theInhibitoryLayer01=InhibitoryLayer(theID=UuidBaptist.Baptize())

theClusterIDSet02=[]
theInhibitoryLayer02=InhibitoryLayer(theID=UuidBaptist.Baptize())

theInhibitoryNeuronIDSet01=[]

for theIndex in range(theNumberClustersPerInhibitoryLayer01):
    theCluster=Cluster(UuidBaptist.Baptize())
    theInhibitoryLayer01.AddCluster(theCluster=theCluster)
    theClusterIDSet01.append(theCluster.GetID())
    
    for theIndexB in range(theNumberNeuronsPerInhibitoryCluster01):
        theInhibitoryNeuron=InhibitoryNeuron(theID=UuidBaptist.Baptize())
        
        theInhibitoryNeuronIDSet01.append(theInhibitoryNeuron.GetID())
        
        theCluster.AddNeuron(theNeuron=theInhibitoryNeuron)
        
        for theInputNeuronID in theInputNeuronIDSet:
            theInhibitoryNeuron.Connect(theNeuron = theInputLayer.GetNeuron(theID=theInputNeuronID))
        
        theInhibitoryNeuron.InitializeWeightSet()

for theIndex in range(theNumberClustersPerInhibitoryLayer02):
    theCluster=Cluster(UuidBaptist.Baptize())
    theInhibitoryLayer02.AddCluster(theCluster=theCluster)
    theClusterIDSet02.append(theCluster.GetID())
    
    for theIndexB in range(theNumberNeuronsPerInhibitoryCluster02):
        theInhibitoryNeuron=InhibitoryNeuron(theID=UuidBaptist.Baptize())
    
        theCluster.AddNeuron(theNeuron=theInhibitoryNeuron)
        
        for theInhibitoryNeuronID in theInhibitoryNeuronIDSet01:
            theInhibitoryNeuron.Connect(theNeuron = theInhibitoryLayer01.GetNeuron(theID=theInhibitoryNeuronID))
        
        theInhibitoryNeuron.InitializeWeightSet()

#%%
theCompetitiveClusterNeuralNetwork=CompetitiveClusteringNeuralNetwork( theID=UuidBaptist.Baptize())

theCompetitiveClusterNeuralNetwork.AddInputLayer(theInputLayer=theInputLayer)

theCompetitiveClusterNeuralNetwork.AddInhibitoryLayer(theInhibitoryLayer=theInhibitoryLayer01)

theCompetitiveClusterNeuralNetwork.AddInhibitoryLayer(theInhibitoryLayer=theInhibitoryLayer02)

theCompetitiveClusterNeuralNetwork.SetOutputLayer(theOutputLayerID=theInhibitoryLayer02.GetID())

#%% MOCK TRAINING HERE      




theInputActivitySet=dict.fromkeys(theInputNeuronIDSet)    

for theIndex in range(100000):

    n=0
        
    theCaseDraw=True#numpy.random.rand()>0.5 #
    
    for theInputNeuronID in theInputNeuronIDSet:       
        if(theCaseDraw):
            theInput=GetDataNoiseUniform()
        else:
            theInput=GetDataFirstOrderPolynomial(n,theNumberNeuronsPerInputLayer)
            n+=1
        theInputActivitySet[theInputNeuronID]=theInput
        
        

    theCompetitiveClusterNeuralNetwork.Load(theInputActivitySet)    
    theCompetitiveClusterNeuralNetwork.Update(theUpdateStrength=theUpdateStrength)
    print(list(theCompetitiveClusterNeuralNetwork.GetActivity(theID=None).values()))
    file = open('output.txt','a') 
    file.write(str(list(theCompetitiveClusterNeuralNetwork.GetActivity(theID=None).values())) + '\n')

    
    file.close() 
     
#%% MOCK CLASSIFICATION
 