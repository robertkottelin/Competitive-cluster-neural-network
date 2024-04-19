mod neuron;
mod cluster;
mod layer;
mod compann;
// mod db;

use compann::COMPANN;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

use rusqlite::{params, Connection, Result};

fn main() -> io::Result<()> {
    let file_path = "formatted_vectors_all.txt";
    let input_file = File::open(Path::new(file_path))?;
    let mut first_line_reader = BufReader::new(&input_file);

    // Read the first line to determine the number of inputs
    let mut first_line = String::new();
    let input_count = match first_line_reader.read_line(&mut first_line) {
        Ok(_) => first_line.trim().split_whitespace().count(),
        Err(e) => return Err(e),
    };

    // Setup the neural network with the determined input_count
    let mut compann = COMPANN::new(
        vec![
            (2, 2, input_count); 2 // X clusters, Y neurons each, dynamically determined input_count, Z layers
        ],
        0.001, // learning_rate
    );

    // Train the network
    for _ in 0..2 {
        let file = File::open(Path::new(file_path))?;
        let reader = BufReader::new(file);
        for line in reader.lines() {
            let line = line?;
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
    }

    // Open a connection to a new or existing SQLite database
    let conn = match Connection::open("network_data.db") {
        Ok(conn) => conn,
        Err(e) => return Err(std::io::Error::new(std::io::ErrorKind::Other, e)),
    };

    // Create a table to store network data
    if let Err(e) = conn.execute(
        "CREATE TABLE IF NOT EXISTS neuron_data (
            layer_id INTEGER,
            cluster_id INTEGER,
            neuron_id INTEGER,
            weights TEXT,
            output REAL
         )",
        [],
    ) {
        return Err(std::io::Error::new(std::io::ErrorKind::Other, e));
    }
    
    // Insert data into the database
    for (i, layer) in compann.layers.iter().enumerate() {
        for (j, cluster) in layer.clusters.iter().enumerate() {
            for (k, neuron) in cluster.neurons.iter().enumerate() {
                let weights_str = format!("{:?}", neuron.weights); // Convert weights to a string
                if let Err(e) = conn.execute(
                    "INSERT INTO neuron_data (layer_id, cluster_id, neuron_id, weights, output) VALUES (?1, ?2, ?3, ?4, ?5)",
                    params![i, j, k, weights_str, neuron.output],
                ) {
                    return Err(std::io::Error::new(std::io::ErrorKind::Other, e));
                }
            }
        }
    }

    Ok(())
}