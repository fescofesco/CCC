use std::{
    fs::{read_to_string, File},
    io::{Read, Write},
};

struct Room {
    x: i32,
    y: i32,
    desks: i32,
}

pub fn run() {
    do_run("example");
    for i in 1..=5 {
        do_run(&i.to_string())
    }
}

pub fn do_run(sublevel: &str) {
    let mut file = File::open(&format!("input/level2/level2_{sublevel}.in")).unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let room_count: i32 = lines.next().unwrap().parse().unwrap();
    let mut rooms = Vec::new();
    for line in lines {
        let mut token: std::str::SplitAsciiWhitespace<'_> = line.split_ascii_whitespace();
        rooms.push(Room {
            x: token.next().unwrap().parse().unwrap(),
            y: token.next().unwrap().parse().unwrap(),
            desks: token.next().unwrap().parse().unwrap(),
        });
    }

    assert!(rooms.len() == room_count as usize);

    let mut outstring = String::new();
    for r in rooms {
        let mut table_id = 1;
        for y in 0..r.y {
            for x in 0..(r.x / 3) {
                outstring.push_str(&format!("{0} {0} {0} ", table_id));
                table_id += 1;
            }
            outstring.push('\n');
        }
        outstring.push('\n');
    }

    let mut outfile = File::create(&format!("output/level2/level2_{sublevel}.out")).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
