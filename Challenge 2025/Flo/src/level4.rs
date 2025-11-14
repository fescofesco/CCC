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
    // for i in 1 ..=5
    // {
    //     do_run(&i.to_string())
    // }
}

pub fn do_run(sublevel: &str) {
    let mut file = File::open(&format!("input/level4/level4_{sublevel}.in")).unwrap();
    let mut filecontent = String::new();
    file.read_to_string(&mut filecontent).unwrap();

    let mut lines = filecontent.lines();
    let room_count: i32 = lines.next().unwrap().parse().unwrap();
    let mut rooms = Vec::new();
    for line in lines {
        let mut token: std::str::SplitAsciiWhitespace<'_> = line.split_ascii_whitespace();
        let x: i32 = token.next().unwrap().parse().unwrap();
        let x_desk = (x + 1) % 4;
        let y_desk = ((x - 1) % 4) / 2 == 0;

        rooms.push(Room {
            x,
            y: token.next().unwrap().parse().unwrap(),
            desks: token.next().unwrap().parse().unwrap(),
        });
    }

    assert!(rooms.len() == room_count as usize);

    let print_horizontal = true;
    let extra = true;

    let mut outstring = String::new();

    let mut num_tables = 0;
    for r in rooms {
        let y_desk = ((r.x - 1) % 4) / 2 == 0;

        for y in 0..r.y {
            for x in 0..(r.x) {
                let mut printx = x % 4 != 3;
                let mut printy = printx;

                let end = (r.x - x) < 3 && y_desk;

                printx &= !end;
                printx &= y % 2 != 1;

                printy &= end;
                printy &= y % 4 != 3;
                printy &= x % 4 == 0;

                if printx && (x % 4 == 0) {
                    num_tables += 1;
                }

                if !printx && printy && (y % 4 == 0) {
                    panic!();
                    num_tables += 1;
                }

                if printx || printy {
                    outstring.push_str("x");
                } else {
                    outstring.push_str(".");
                }
            }

            outstring.push('\n');
        }
        assert_eq!(num_tables, r.desks);
        outstring.push('\n');
    }

    let mut outfile = File::create(&format!("output/level4/level4_{sublevel}.out")).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
