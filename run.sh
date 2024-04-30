#!/bin/bash

# Check if cargo is installed
if ! command -v cargo &> /dev/null
then
    echo "cargo could not be found, please install Rust and Cargo."
    exit
fi

# Build the project
echo "Building the project..."
cargo build --release

# Run the built executable
echo "Running the blockchain simulation..."
./target/release/code-challenge-2024-SkyWarrior123

