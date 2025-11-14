use std::{
    fs::{self, File, read_to_string},
    io::{Read, Write},
};

struct TimeDistance
{
    time : i32,
    distance : i32,
}

pub fn part1() {
    // let filename = "level1_1_small";
    let filename = "level2_0_example";
    let level = "level2";

    let mut file = File::open(format!("./../Input/{level}/{filename}.in")).unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let number_manover: i32 = lines.next().unwrap().parse().unwrap();
    let mut manover_totals = Vec::new();
    for manover in lines {

        let mut time = 0;
        let mut distance = 0;
        for pace_str in  manover.split_ascii_whitespace()
        {
            let pace = pace_str.parse::<i32>().unwrap();
            distance += pace.signum();
            if pace == 0 {
                time += 1;
            } 
            else {
                time += pace.abs();
            }           
        }

        manover_totals.push(TimeDistance{time, distance});
        
    }

    assert!(manover_totals.len() == number_manover as usize);

    let mut outstring = String::new();
    for m in manover_totals {
        outstring.push_str(&format!("{0} {1}\n", m.distance, m.time));
    }

    std::fs::create_dir_all(format!("output/{level}")).unwrap();
    let mut outfile = File::create(format!("output/{level}/{filename}.out")).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
