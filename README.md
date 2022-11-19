# Competitive-cluster-neural-network
Unsupervised deep neural network to learn and detect liquidity patterns

Each cluster will only fire one neuron, and the neuron that does fire also
diminishes the output of all other neurons in that cluster through inhibitory connections. Each neuron
in layer i is connected to every neuron in the subsequent layer j. For every neuron in the second and
higher layers, the total weight of 1.0 is distributed randomly across all incoming connections (ΣiWij=1).
These weights are updated for the j-th layer neurons only if they display the maximum output in their
respective clusters. The weight update is the following: zero, if the neuron does not have the maximum
output of its cluster, or g(cjk/nk) – gwij if the neuron has the maximum output of its cluster. Where g is
a constant representing the learning rate (also called learning strength or update strength and depicts
how much the weights and biases are updated for each iteration), cjk is one if the j-th element of the
presented stimulus pattern, Sk, is 1. Otherwise, cjk is 0, nk is the number of active neurons in the input
layer (i.e., the number of activated floats between 0-1s in Sk). When an input excites neurons in the
input layer L1, the output from these neurons travel and excite neurons in the L2 layer. The neurons
with the highest outputs in L2 will 1) fire and excite neurons in the next and, in this case, final layer
and 2) send inhibitory signals to the other neurons in the same cluster. The neuron that displays the
maximum activation in each cluster will have its incoming connection weights updated so that the
active connections get strengthened at the expense of less active connections so that the weighted sum
of each neuron will remain at 1.0. In other words, the weight change of – gwij is taken from the lowest
activated neuron and redistributed evenly across the active inputs; this results in a scenario where the
neurons displaying the highest output will fire easier and display an even higher activation level when
a similar input pattern is presented to the network. The idea is that updating the connection weights
and indirectly, therefore each respective clusters’ neuron activity will create a specific “firing”
fingerprint of the network for each group of input patterns existing in the input data.
![image](https://user-images.githubusercontent.com/74188272/201863534-f9b1f21c-fcd5-4c66-943e-edd98ed8da30.png)
