use std::{
    fs::{read_to_string, File},
    io::{Read, Write},
};

struct Room {
    x_desk: i32,
    x_remainder: i32,
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
    let mut file = File::open(&format!("input/level3/level3_{sublevel}.in")).unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let room_count: i32 = lines.next().unwrap().parse().unwrap();
    let mut rooms = Vec::new();
    for line in lines {
        let mut token: std::str::SplitAsciiWhitespace<'_> = line.split_ascii_whitespace();
        let x: i32 = token.next().unwrap().parse().unwrap();
        let x_desk = x / 3;
        let x_remainder = x % 3;
        rooms.push(Room {
            x_desk,
            x_remainder,
            y: token.next().unwrap().parse().unwrap(),
            desks: token.next().unwrap().parse().unwrap(),
        });
    }

    assert!(rooms.len() == room_count as usize);

    let mut outstring = String::new();
    for r in rooms {
        let mut table_id_x = 1;
        let mut table_id_y = r.desks;

        let y_desks = r.y / 3;
        let y_filled = y_desks * 3;
        for y in 0..r.y {
            for x in 0..(r.x_desk) {
                outstring.push_str(&format!("{0} {0} {0} ", table_id_x));
                table_id_x += 1;
            }

            for i in 0..(r.x_remainder) {
                if y < y_filled {
                    outstring.push_str(&format!("{0} ", table_id_y - i));
                } else {
                    outstring.push_str(&format!("0 "));
                }
            }

            if y % 3 == 2 {
                table_id_y -= r.x_remainder;
            }
            outstring.push('\n');
        }
        outstring.push('\n');
    }

    let mut outfile = File::create(&format!("output/level3/level3_{sublevel}.out")).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
