mod neuron;
mod cluster;
mod layer;
mod compann;
// mod db;

use compann::COMPANN;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

extern crate serde;
extern crate serde_json;

use rusqlite::{params, Connection, Result as SqliteResult, types::Type};

// Function to load neuron data from the database
pub fn load_neuron_data(conn: &Connection) -> SqliteResult<Vec<(usize, usize, usize, Vec<f64>, f64)>> {
    let mut stmt = conn.prepare("SELECT layer_id, cluster_id, neuron_id, weights, output FROM neuron_data")?;
    let neuron_iter = stmt.query_map([], |row| {
        Ok((
            row.get(0)?,
            row.get(1)?,
            row.get(2)?,
            serde_json::from_str::<Vec<f64>>(&row.get::<_, String>(3)?)
                .map_err(|_e| rusqlite::Error::InvalidColumnType(3, "weights".into(), Type::Text))?, // Correct error type
            row.get(4)?
        ))
    })?;

    let mut neurons = Vec::new();
    for neuron in neuron_iter {
        neurons.push(neuron?);
    }
    Ok(neurons)
}


pub fn open_connection(db_path: &str) -> Result<Connection, rusqlite::Error> {
    Connection::open(db_path)
}

fn insert_classification_result(conn: &Connection, id: i64, result: &str) -> SqliteResult<()> {
    conn.execute(
        "INSERT INTO results (id, result) VALUES (?1, ?2)",
        params![id, result],
    )?;
    Ok(())
}


fn main() -> io::Result<()> {
    let file_path = "formatted_vectors_all.txt";
    let input_file = File::open(Path::new(file_path))?;
    let mut first_line_reader = BufReader::new(&input_file);

    // Read the first line to determine the number of inputs
    let mut first_line = String::new();
    let input_count = first_line_reader.read_line(&mut first_line)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
    
    // Setup the neural network with the determined input_count
    let mut compann = COMPANN::new(
        vec![
            (20, 20, input_count); 10 // X clusters, Y neurons each, dynamically determined input_count, Z layers
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

    if let Err(e) = conn.execute(
        "CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            result TEXT
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

    // Load the network data from the database
    let neurons_data = load_neuron_data(&conn)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
    
    for (layer_id, cluster_id, neuron_id, weights, output) in neurons_data {
        compann.set_neuron_data(layer_id, cluster_id, neuron_id, weights, output)
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
    }

    // Classify patterns in "formatted_vectors_all.txt"
    // Use the classify function in the main program
    let file = File::open(Path::new(file_path))?;
    let reader = BufReader::new(file);
    let mut id = 0;
    for line in reader.lines() {
        let line = line?;
        let vector: Result<Vec<f64>, _> = line.split_whitespace().map(|s| s.parse()).collect();
        match vector {
            Ok(input_pattern) => {
                let classification_results = compann.classify(input_pattern);
                let results_str = format!("{:?}", classification_results);
                
                // Insert the results into the database
                insert_classification_result(&conn, id, &results_str)
                    .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
                
                id += 1; // Increment the identifier for the next result
            },
            Err(e) => {
                eprintln!("Could not parse line '{}': {}", line, e);
            },
        }
    }

    Ok(())
}