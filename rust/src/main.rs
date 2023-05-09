use std::fmt;
use std::fs::File;
use std::io::{self, BufRead, LineWriter, Write};
use std::path::Path;
use std::cmp::Ordering;
use rand::prelude::*;

// Define a struct to represent a neuron
#[derive(Debug)]
struct Neuron {
    weights: Vec<f64>, // The neuron's weights
    output: f64, // The neuron's output
}

impl Neuron {
    // Constructor for the neuron
    fn new(input_count: usize) -> Neuron {
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
    fn activate(&mut self, inputs: &Vec<f64>) {
        // Compute the net input to the neuron
        let net_input: f64 = self.weights.iter().zip(inputs.iter()).map(|(w, i)| w * i).sum();
        // Compute the output of the neuron using the sigmoid function
        self.output = 1.0 / (1.0 + (-net_input).exp());
    }
    
    // Update function for the neuron's weights
    fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64, cjk: f64, nk: f64) {
        // Iterate over the neuron's weights and inputs in parallel, updating each weight
        self.weights.iter_mut().zip(inputs.iter()).for_each(|(w, _)| {
            // Compute the gradient of the output with respect to the weight
            let gwij = self.output * *w;
            // Update the weight using the gradient and the learning rate
            *w += learning_rate * (cjk / nk - gwij);
        });
    }
}
// Define a struct to represent a cluster of neurons
#[derive(Debug)]
struct Cluster {
    neurons: Vec<Neuron>, // A cluster consists of multiple neurons
}

impl Cluster {
    // Define a constructor method for the Cluster struct that takes in the number of neurons and number of inputs
    // for each neuron and returns a new Cluster instance with randomly initialized neurons
    fn new(neuron_count: usize, input_count: usize) -> Cluster {
        let neurons = (0..neuron_count).map(|_| Neuron::new(input_count)).collect();
        Cluster { neurons }
    }

    // Define a method to activate the neurons in the cluster given a vector of input values
    fn activate(&mut self, inputs: &Vec<f64>) {
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
    fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64) {
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

#[derive(Debug)]
struct Layer {
    clusters: Vec<Cluster>,
}

impl Layer {
    // Creates a new `Layer` with the given number of `clusters`, `neurons` and `inputs`
    fn new(cluster_count: usize, neuron_count: usize, input_count: usize) -> Layer {
        // Create `cluster_count` number of `Cluster`s, each with `neuron_count` number of `Neuron`s
        let clusters = (0..cluster_count).map(|_| Cluster::new(neuron_count, input_count)).collect();
        Layer { clusters }
    }

    // Activates each `Cluster` in the `Layer` with the given `inputs`
    fn activate(&mut self, inputs: &Vec<f64>) {
        self.clusters.iter_mut().for_each(|c| c.activate(inputs));
    }

    // Updates the weights of each `Cluster` in the `Layer` with the given `inputs` and `learning_rate`
    fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64) {
        self.clusters.iter_mut().for_each(|c| c.update_weights(inputs, learning_rate));
    }
}

#[derive(Debug)]
struct COMPANN {
    layers: Vec<Layer>,
    learning_rate: f64,
}

impl COMPANN {
    // Creates a new `COMPANN` with the given `layer_sizes` and `learning_rate`
    fn new(layer_sizes: Vec<(usize, usize, usize)>, learning_rate: f64) -> COMPANN {
        // Create a `Layer` for each `(clusters, neurons, inputs)` tuple in `layer_sizes`
        let layers: Vec<Layer> = layer_sizes.iter().map(|&(clusters, neurons, inputs)| Layer::new(clusters, neurons, inputs)).collect();
        COMPANN { layers, learning_rate }
    }

    // Trains the `COMPANN` with the given `input_pattern`
    fn train(&mut self, input_pattern: Vec<f64>) {
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



fn main() -> io::Result<()> {
    let mut compann = COMPANN::new(
        vec![
            (20, 20, 100); 20 // 20 clusters, 20 neurons each, 100 input neurons, 20 layers
        ],
        0.001, // learning_rate
    );

    // Generate a random line as input
    let mut rng = thread_rng();
    let inclinations = [-45.0, 45.0];
    let inclination = inclinations.choose(&mut rng).unwrap();
    
    let line_func = match inclination {
        45.0 => |x| x,
        -45.0 => |x| 100.0 - x,
        _ => unreachable!(),
    };

    let inputs: Vec<f64> = (0..100).map(|x| line_func(x as f64)).collect();
    // Print the input vector
    println!("{:?}", inputs);

    // Train the network on the input vector
    for _ in 0..10000 {
        compann.train(inputs.clone());
    }
    
    /* Train on formatted vectors as input
    let file = File::open(Path::new("formatted_vectors.txt"))?;

    let reader = io::BufReader::new(file);

    for line in reader.lines() {
        let line = line?;
        // Split the line into numbers, parse each number into a float, and collect into a vector
        let vector: Result<Vec<f64>, _> = line.split_whitespace().map(|s| s.parse()).collect();
        match vector {
            Ok(input_pattern) => {
                compann.train(input_pattern);
            },
            Err(e) => {
                eprintln!("Could not parse line '{}': {}", line, e);
            },
        }
    }
    */

    // Write the trained network to a file named 'output.txt'
    let mut output_file = LineWriter::new(File::create("output.txt")?);
    write!(output_file, "{}", compann.to_string())?;

    Ok(())
}