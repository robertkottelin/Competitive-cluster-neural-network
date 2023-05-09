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
        let weights: Vec<f64> = (0..input_count).map(|_| rng.gen()).collect();
        let total_weight: f64 = weights.iter().sum();
        let normalized_weights: Vec<f64> = weights.iter().map(|w| w / total_weight).collect();

        Neuron {
            weights: normalized_weights,
            output: 0.0,
        }
    }

    fn activate(&mut self, inputs: &Vec<f64>) {
        self.output = self.weights.iter().zip(inputs.iter()).map(|(w, i)| w * i).sum();
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

fn main() {
    let mut compann = COMPANN::new(
        vec![
            (2, 3, 3), // 2 clusters, 3 neurons each, 3 inputs each
            (2, 3, 2), // 2 clusters, 3 neurons each, 2 inputs each
        ],
        0.1, // learning_rate
    );

    let input_patterns = vec![
        vec![0.1, 0.2, 0.7],
        vec![0.3, 0.3, 0.4],
        vec![0.6, 0.2, 0.2],
    ];

    for pattern in input_patterns {
        compann.train(pattern);
    }

    println!("{:?}", compann);
}
