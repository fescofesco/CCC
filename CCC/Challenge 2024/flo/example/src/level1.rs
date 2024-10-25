use std::{fs::{read_to_string, File}, io::{Read, Write}};

struct Room
{
    x : u32,
    y : u32
}

pub fn part1()
{
    let mut file = File::open("input/level1/level1_1.in").unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let room_count : i32 = lines.next().unwrap().parse().unwrap();
    let mut rooms = Vec::new();
    for line in lines {
        let mut token: std::str::SplitAsciiWhitespace<'_> = line.split_ascii_whitespace();
        rooms.push(Room{
            x : token.next().unwrap().parse().unwrap(),
            y : token.next().unwrap().parse().unwrap(),
        });
    }

    assert!(rooms.len() == room_count as usize);

    let mut outstring = String::new();
    for r in rooms {

        outstring.push_str(&format!("{0}\n", (r.x / 3) * r.y));
    }

    let mut outfile = File::create("output/level1/level1_1.out").unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}