use crate::transaction::Transaction;

pub struct Block {
    pub header: String, // Simplified header; realistically would include merkle root, previous block hash, etc.
    pub transactions: Vec<Transaction>,
}

pub struct Blockchain;

impl Blockchain {
    pub fn new() -> Self {
        Blockchain
    }

    pub fn mine_block(&self, transactions: Vec<Transaction>) -> Block {
        let valid_transactions: Vec<Transaction> = transactions.into_iter().filter(|tx| tx.is_valid()).collect();
        let header = format!("Block with {} transactions", valid_transactions.len());
        Block { header, transactions: valid_transactions }
    }
}
