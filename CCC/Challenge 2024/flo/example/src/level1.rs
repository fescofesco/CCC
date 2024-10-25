use std::{fs::{read_to_string, File}, io::{Read, Write}};

pub fn part1()
{
    let mut file = File::open("input/level1/level1_1.in").unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();

    let mut outstring = String::new();
    for line in lines {
        outstring.push_str(&format!("{0}\n", line));
    }

    let mut outfile = File::create("output/level1/level1_1.out").unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}