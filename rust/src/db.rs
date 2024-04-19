use rusqlite::{params, Connection, Result};
use std::io;

// Function to open a connection to the SQLite database.
pub fn open_connection(db_path: &str) -> Result<Connection, rusqlite::Error> {
    Connection::open(db_path)
}

// Function to create the necessary tables for storing neuron data.
pub fn create_tables(conn: &Connection) -> Result<(), rusqlite::Error> {
    conn.execute(
        "CREATE TABLE IF NOT EXISTS neuron_data (
            layer_id INTEGER,
            cluster_id INTEGER,
            neuron_id INTEGER,
            weights TEXT,
            output REAL
        )",
        [],
    )?;
    Ok(())
}

// Function to insert neuron data into the database.
pub fn insert_neuron_data(
    conn: &Connection,
    layer_id: usize,
    cluster_id: usize,
    neuron_id: usize,
    weights: &str,
    output: f64,
) -> Result<(), rusqlite::Error> {
    conn.execute(
        "INSERT INTO neuron_data (layer_id, cluster_id, neuron_id, weights, output) VALUES (?1, ?2, ?3, ?4, ?5)",
        params![layer_id, cluster_id, neuron_id, weights, output],
    )?;
    Ok(())
}
