use rand::prelude::*;
use std::vec::Vec;

#[derive(Debug)]
pub struct Neuron {
    pub weights: Vec<f64>,
    pub output: f64,
}

impl Neuron {
    pub fn new(input_count: usize) -> Neuron {
        let mut rng = thread_rng(); // Initialize a random number generator
        let mut weights: Vec<f64>; // Declare a vector to hold the neuron's weights
        let mut total_weight: f64; // Declare a variable to hold the total weight of the neuron's inputs
        loop {
            // Generate a vector of random weights for the neuron's inputs
            weights = (0..input_count).map(|_| rng.gen_range(-0.1..=0.1)).collect();
            
            // Compute the total weight of the neuron's inputs
            total_weight = weights.iter().sum();
            // If the total weight is not too small (to avoid division by zero), break out of the loop
            if total_weight.abs() > 1e-6 { // Use an epsilon to account for floating-point error
                break;
            }
        }
        // Normalize the weights so that their sum is 1
        let normalized_weights: Vec<f64> = weights.iter().map(|w| w / total_weight).collect();

        // Return the neuron with its weights and output initialized
        Neuron {
            weights: normalized_weights,
            output: 0.0,
        }
    }

    // Activation function for the neuron
    pub fn activate(&mut self, inputs: &Vec<f64>) {
        // Compute the net input to the neuron
        let net_input: f64 = self.weights.iter().zip(inputs.iter()).map(|(w, i)| w * i).sum();
        // Compute the output of the neuron using the sigmoid function
        self.output = 1.0 / (1.0 + (-net_input).exp());
    }
    
    // Update function for the neuron's weights
    pub fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64, cjk: f64, nk: f64) {
        // Iterate over the neuron's weights and inputs in parallel, updating each weight
        self.weights.iter_mut().zip(inputs.iter()).for_each(|(w, _)| {
            // Compute the gradient of the output with respect to the weight
            let gwij = self.output * *w;
            // Update the weight using the gradient and the learning rate
            *w += learning_rate * (cjk / nk - gwij);
        });
    }
}



