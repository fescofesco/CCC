use std::{
    default,
    fs::{read_to_string, File},
    io::{Read, Write},
};

struct Room {
    x: i32,
    y: i32,
    desks: i32,
}

pub fn run() {
}

#[derive(Clone, Copy, Default, PartialEq, Eq)]
enum Field {
    #[default]
    None,
    X,
    WTF,
    Empty,
}
