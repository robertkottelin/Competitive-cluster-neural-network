# -*- coding: utf-8 -*-


from NeuronSet import NeuronSet

class InputLayer(NeuronSet):
    
    def __init__(self,theID : str):
        super(InputLayer,self).__init__(theID=theID)
    
    def SetActivity(self,theID: str,theActivity: float) -> None:
        if(not self.HasNeuron(theID=theID)):
            return None
        else:
            self.GetNeuron(theID=theID).SetActivity(theActivity=theActivity)
    
    def GetActivity(self,theID : str) -> float:
        if(not self.HasNeuron(theID=theID)):
            return None
        else:
            return self.GetNeuron(theID=theID).GetActivity()
    