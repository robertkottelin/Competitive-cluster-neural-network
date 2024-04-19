use crate::neuron::Neuron;
use std::vec::Vec;
use std::cmp::Ordering;

// Define a struct to represent a cluster of neurons
#[derive(Debug)]
pub struct Cluster {
    pub neurons: Vec<Neuron>, // A cluster consists of multiple neurons
}

impl Cluster {
    // Define a constructor method for the Cluster struct that takes in the number of neurons and number of inputs
    // for each neuron and returns a new Cluster instance with randomly initialized neurons
    pub fn new(neuron_count: usize, input_count: usize) -> Cluster {
        let neurons = (0..neuron_count).map(|_| Neuron::new(input_count)).collect();
        Cluster { neurons }
    }

    // Define a method to activate the neurons in the cluster given a vector of input values
    pub fn activate(&mut self, inputs: &Vec<f64>) {
        // Activate each neuron in the cluster with the given input vector
        self.neurons.iter_mut().for_each(|n| n.activate(inputs));
        
        // Find the neuron with the highest output value (i.e., the "winner") and set all other neurons' outputs to zero
        let max_output_index = self.neurons.iter().enumerate()
            .max_by(|(_, a), (_, b)| a.output.partial_cmp(&b.output).unwrap_or(Ordering::Equal))
            .map(|(index, _)| index) // Get the index of the winning neuron
            .unwrap_or(0); // If there is no winner, use the first neuron as the winner
        for (index, neuron) in self.neurons.iter_mut().enumerate() {
            if index != max_output_index { // If the neuron is not the winner, set its output to zero
                neuron.output = 0.0;
            }
        }
    }

    // Define a method to update the weights of each neuron in the cluster given a vector of input values and a learning rate
    pub fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64) {
        // Find the neuron with the highest output value (i.e., the "winner")
        let max_output_index = self.neurons.iter().enumerate()
            .max_by(|(_, a), (_, b)| a.output.partial_cmp(&b.output).unwrap_or(Ordering::Equal))
            .map(|(index, _)| index)
            .unwrap_or(0);
        // Count the number of neurons in the cluster with non-zero outputs
        let nk = self.neurons.iter().filter(|n| n.output > 0.0).count() as f64;
        // For each neuron in the cluster, update its weights using the delta rule if it is the winner neuron, or set its
        // output to zero if it is not the winner neuron
        for (index, neuron) in self.neurons.iter_mut().enumerate() {
            if index != max_output_index { // If the neuron is not the winner, set its output to zero
                neuron.output = 0.0;
            } else { // If the neuron is the winner, update its weights using the delta rule
                let cjk = if neuron.output > 0.0 { 1.0 } else { 0.0 }; // Set cjk to 1 if the neuron is active, 0 otherwise
                neuron.update_weights(inputs, learning_rate, cjk, nk);
            }
        }
    }
}