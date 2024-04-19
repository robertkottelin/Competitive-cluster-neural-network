use crate::cluster::Cluster;
use std::vec::Vec;

#[derive(Debug)]
pub struct Layer {
    pub clusters: Vec<Cluster>,
}

impl Layer {
    // Creates a new `Layer` with the given number of `clusters`, `neurons` and `inputs`
    pub fn new(cluster_count: usize, neuron_count: usize, input_count: usize) -> Layer {
        // Create `cluster_count` number of `Cluster`s, each with `neuron_count` number of `Neuron`s
        let clusters = (0..cluster_count).map(|_| Cluster::new(neuron_count, input_count)).collect();
        Layer { clusters }
    }

    // Activates each `Cluster` in the `Layer` with the given `inputs`
    pub fn activate(&mut self, inputs: &Vec<f64>) {
        self.clusters.iter_mut().for_each(|c| c.activate(inputs));
    }

    // Updates the weights of each `Cluster` in the `Layer` with the given `inputs` and `learning_rate`
    pub fn update_weights(&mut self, inputs: &Vec<f64>, learning_rate: f64) {
        self.clusters.iter_mut().for_each(|c| c.update_weights(inputs, learning_rate));
    }
}