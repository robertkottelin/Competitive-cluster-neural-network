use std::fmt;
use std::fs::File;
use std::io::{self, BufRead, LineWriter, Write};
use std::path::Path;
use std::cmp::Ordering;
use rand::prelude::*;

#[derive(Debug)]
struct Neuron {
    weights: Vec<f64>,
    output: f64,
}

impl Neuron {
    fn new(input_count: usize) -> Neuron {
        let mut rng = thread_rng();
        let mut weights: Vec<f64>;
        let mut total_weight: f64;
        loop {
            weights = (0..input_count).map(|_| rng.gen_range(-0.1..=0.1)).collect();
            total_weight = weights.iter().sum();
            if total_weight.abs() > 1e-6 { // Use an epsilon to account for floating-point error
                break;
            }
        }
        let normalized_weights: Vec<f64> = weights.iter().map(|w| w / total_weight).collect();

        Neuron {
            weights: normalized_weights,
            output: 0.0,
        }
    }

    fn activate(&mut self, inputs: &Vec<f64>) {
        let net_input: f64 = self.weights.iter().zip(inputs.iter()).map(|(w, i)| w * i).sum();
        self.output = 1.0 / (1.0 + (-net_input).exp());
    }
    
    fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64, cjk: f64, nk: f64) {
        self.weights.iter_mut().zip(inputs.iter()).for_each(|(w, _)| {
            let gwij = self.output * *w;
            *w += learning_rate * (cjk / nk - gwij);
        });
    }
}

#[derive(Debug)]
struct Cluster {
    neurons: Vec<Neuron>,
}

impl Cluster {
    fn new(neuron_count: usize, input_count: usize) -> Cluster {
        let neurons = (0..neuron_count).map(|_| Neuron::new(input_count)).collect();
        Cluster { neurons }
    }

    fn activate(&mut self, inputs: &Vec<f64>) {
        self.neurons.iter_mut().for_each(|n| n.activate(inputs));
        
        let max_output_index = self.neurons.iter().enumerate()
            .max_by(|(_, a), (_, b)| a.output.partial_cmp(&b.output).unwrap_or(Ordering::Equal))
            .map(|(index, _)| index)
            .unwrap_or(0);
        for (index, neuron) in self.neurons.iter_mut().enumerate() {
            if index != max_output_index {
                neuron.output = 0.0;
            }
        }
    }

    fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64) {
        let max_output_index = self.neurons.iter().enumerate()
            .max_by(|(_, a), (_, b)| a.output.partial_cmp(&b.output).unwrap_or(Ordering::Equal))
            .map(|(index, _)| index)
            .unwrap_or(0);
        let nk = self.neurons.iter().filter(|n| n.output > 0.0).count() as f64;
        for (index, neuron) in self.neurons.iter_mut().enumerate() {
            if index != max_output_index {
                neuron.output = 0.0;
            } else {
                let cjk = if neuron.output > 0.0 { 1.0 } else { 0.0 };
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
    fn new(cluster_count: usize, neuron_count: usize, input_count: usize) -> Layer {
        let clusters = (0..cluster_count).map(|_| Cluster::new(neuron_count, input_count)).collect();
        Layer { clusters }
    }

    fn activate(&mut self, inputs: &Vec<f64>) {
        self.clusters.iter_mut().for_each(|c| c.activate(inputs));
    }

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
    fn new(layer_sizes: Vec<(usize, usize, usize)>, learning_rate: f64) -> COMPANN {
        let layers: Vec<Layer> = layer_sizes.iter().map(|&(clusters, neurons, inputs)| Layer::new(clusters, neurons, inputs)).collect();
        COMPANN { layers, learning_rate }
    }

    fn train(&mut self, input_pattern: Vec<f64>) {
        let input_pattern_cloned = input_pattern.clone();  // clone the input_pattern
        let mut inputs = input_pattern;
        for layer in &mut self.layers {
            layer.activate(&inputs);
            inputs = layer.clusters.iter().map(|c| c.neurons.iter().map(|n| n.output).sum()).collect();
        }

        inputs = input_pattern_cloned;
        for layer in &mut self.layers {
            layer.update_weights(&inputs, self.learning_rate);
            inputs = layer.clusters.iter().map(|c| c.neurons.iter().map(|n| n.output).sum()).collect();
        }
    }
}

impl fmt::Display for COMPANN {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "COMPANN {{\n")?;
        for (i, layer) in self.layers.iter().enumerate() {
            write!(f, "    Layer {} {{\n", i)?;
            for (j, cluster) in layer.clusters.iter().enumerate() {
                write!(f, "        Cluster {} {{\n", j)?;
                for (k, neuron) in cluster.neurons.iter().enumerate() {
                    write!(f, "            Neuron {} {{\n                Weights: {:?}\n                Output: {}\n            }}\n", k, neuron.weights, neuron.output)?;
                }
                write!(f, "        }}\n")?;
            }
            write!(f, "    }}\n")?;
        }
        write!(f, "}}\n")?;
        Ok(())
    }
}


fn main() -> io::Result<()> {
    let mut compann = COMPANN::new(
        vec![
            (10, 5, 100); 5 // 10 clusters, 5 neurons each, 100 inputs each for 5 layers
        ],
        0.001, // learning_rate
    );

    // // Open the file
    // let file = File::open(Path::new("formatted_vectors.txt"))?;

    // // Create a BufReader for the file
    // let reader = io::BufReader::new(file);

    // // Read each line
    // for line in reader.lines() {
    //     let line = line?;
    //     // Split the line into numbers, parse each number into a float, and collect into a vector
    //     let vector: Result<Vec<f64>, _> = line.split_whitespace().map(|s| s.parse()).collect();
    //     match vector {
    //         Ok(input_pattern) => {
    //             compann.train(input_pattern);
    //         },
    //         Err(e) => {
    //             eprintln!("Could not parse line '{}': {}", line, e);
    //         },
    //     }
    // }

    // Generate random line as input
    let mut rng = thread_rng();
    let inclinations = [-45.0, 45.0];
    let inclination = inclinations.choose(&mut rng).unwrap();
    
    let line_func = match inclination {
        45.0 => |x| x,
        -45.0 => |x| 100.0 - x,
        _ => unreachable!(),
    };

    let inputs: Vec<f64> = (0..100).map(|x| line_func(x as f64)).collect();
    // print input
    println!("{:?}", inputs);

    // Train network on line
    for _ in 0..10000 {
        compann.train(inputs.clone());
    }

    println!("{:?}", compann);

    let mut output_file = LineWriter::new(File::create("output.txt")?);
    // Write the output to a file
    write!(output_file, "{}", compann.to_string())?;

    Ok(())
}