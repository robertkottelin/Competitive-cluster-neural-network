# Competitive-cluster-neural-network
Unsupervised deep neural network to learn and detect liquidity patterns

The design of a competitive clustering network. Input excites certain neurons at 
the first layer. The outputs from these neurons are amplified and set to clusters of nodes in 
the second and higher layers in a hierarchy where only a single node in each cluster "fires." 
Further, nodes within the same cluster can be connected to other nodes in that cluster with 
inhibitory weights. Over successive presentations of input patterns, the network transitions 
to a "firing pattern" associated with each input. When new inputs are offered to the network, 
the hope is that the network will again exhibit the same firing patterns for inputs that are 
"close" to those that it has already observed. 

Small scale example of architecture:

![image](https://user-images.githubusercontent.com/74188272/201863534-f9b1f21c-fcd5-4c66-943e-edd98ed8da30.png)
