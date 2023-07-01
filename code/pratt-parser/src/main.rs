use pratt_parser::expr;
use std::io::{stdin, BufRead};

fn main() {
    for line in stdin().lock().lines() {
        let line = line.unwrap();
        let s = expr(&line);
        println!("{}", s);
    }
}
