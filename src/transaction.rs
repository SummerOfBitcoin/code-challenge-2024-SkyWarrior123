use serde::{Deserialize, Serialize};
use serde_json::{Result, Value};
use std::fs::File;
use std::io::Read;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Transaction {
    version: i32,
    locktime: u32,
    vin: Vec<Input>,
    vout: Vec<Output>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Input {
    txid: String,
    vout: u32,
    prevout: PrevOut,
    scriptsig: String,
    scriptsig_asm: String,
    witness: Vec<String>,
    is_coinbase: bool,
    sequence: u32,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct PrevOut {
    scriptpubkey: String,
    scriptpubkey_asm: String,
    scriptpubkey_type: String,
    scriptpubkey_address: String,
    value: u64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Output {
    scriptpubkey: String,
    scriptpubkey_asm: String,
    scriptpubkey_type: String,
    scriptpubkey_address: String,
    value: u64,
}

impl Transaction {
    pub fn new_from_file(file_path: &str) -> Result<Self> {
        let mut file = File::open(file_path).expect("file not found");
        let mut contents = String::new();
        file.read_to_string(&mut contents).expect("something went wrong reading the file");
        serde_json::from_str::<Transaction>(&contents)
    }

    pub fn is_valid(&self) -> bool {
        // Basic validation: Check if all inputs have valid txid formats and if the outputs do not exceed input values.
        // More complex validations like script and signature verifications are omitted for simplicity.
        self.vin.iter().all(|input| hex::decode(&input.txid).is_ok()) &&
        !self.vin.is_empty() && !self.vout.is_empty() &&
        self.total_input_value() >= self.total_output_value()
    }

    fn total_input_value(&self) -> u64 {
        self.vin.iter().map(|input| input.prevout.value).sum()
    }

    fn total_output_value(&self) -> u64 {
        self.vout.iter().map(|output| output.value).sum()
    }
}

