use std::{
    fs::{self, File, read_to_string},
    io::{Read, Write},
};



pub fn part1() {
    // let filename = "level1_1_small";
    let filename = "level1_2_large";

    let mut file = File::open(format!("./../Input/level1/{0}.in", filename)).unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let number_manover: i32 = lines.next().unwrap().parse().unwrap();
    let mut manover_totals = Vec::new();
    for manover in lines {

        let mut paceval = 0;
        for pace in  manover.split_ascii_whitespace()
        {
            paceval += pace.parse::<i32>().unwrap();
        }

        manover_totals.push(paceval);
        
    }

    assert!(manover_totals.len() == number_manover as usize);

    let mut outstring = String::new();
    for m in manover_totals {
        outstring.push_str(&format!("{0}\n", m));
    }

    std::fs::create_dir_all("output/level1/").unwrap();
    let mut outfile = File::create(format!("output/level1/{0}.out", filename)).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
