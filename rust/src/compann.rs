use crate::layer::Layer;
use std::vec::Vec;
use std::fmt;

#[derive(Debug)]
pub struct COMPANN {
    pub layers: Vec<Layer>,
    pub learning_rate: f64,
}

impl COMPANN {
    // Creates a new `COMPANN` with the given `layer_sizes` and `learning_rate`
    pub fn new(layer_sizes: Vec<(usize, usize, usize)>, learning_rate: f64) -> COMPANN {
        // Create a `Layer` for each `(clusters, neurons, inputs)` tuple in `layer_sizes`
        let layers: Vec<Layer> = layer_sizes.iter().map(|&(clusters, neurons, inputs)| Layer::new(clusters, neurons, inputs)).collect();
        COMPANN { layers, learning_rate }
    }

    // Trains the `COMPANN` with the given `input_pattern`
    pub fn train(&mut self, input_pattern: Vec<f64>) {
        let input_pattern_cloned = input_pattern.clone();  
        let mut inputs = input_pattern;
        for layer in &mut self.layers {
            // Activate each `Cluster` in the current `Layer` with the current `inputs`
            layer.activate(&inputs);
            // Sum the `output` of each `Neuron` in each `Cluster` to get the new `inputs`
            inputs = layer.clusters.iter().map(|c| c.neurons.iter().map(|n| n.output).sum()).collect();
        }

        // Reset inputs to the original input pattern and update weights in reverse order
        inputs = input_pattern_cloned;
        for layer in self.layers.iter_mut().rev() {
            // Update the weights of each `Cluster` in the current `Layer` with the current `inputs`
            layer.update_weights(&inputs, self.learning_rate);
            // Sum the `output` of each `Neuron` in each `Cluster` to get the new `inputs`
            inputs = layer.clusters.iter().map(|c| c.neurons.iter().map(|n| n.output).sum()).collect();
        }
    }
}

impl fmt::Display for COMPANN {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "COMPANN {{\n")?; // start writing "COMPANN {{" in the output
        for (i, layer) in self.layers.iter().enumerate() { // iterate over all layers in the network
            write!(f, "    Layer {} {{\n", i)?; // start writing "Layer i {{" in the output
            for (j, cluster) in layer.clusters.iter().enumerate() { // iterate over all clusters in the current layer
                write!(f, "        Cluster {} {{\n", j)?; // start writing "Cluster j {{" in the output
                for (k, neuron) in cluster.neurons.iter().enumerate() { // iterate over all neurons in the current cluster
                    write!(f, "            Neuron {} {{\n                Weights: {:?}\n                Output: {}\n            }}\n", k, neuron.weights, neuron.output)?; // write neuron weights and output in the output
                }
                write!(f, "        }}\n")?; // end the current cluster block in the output
            }
            write!(f, "    }}\n")?; // end the current layer block in the output
        }
        write!(f, "}}\n")?; // end the network block in the output
        Ok(()) // indicate success
    }
}