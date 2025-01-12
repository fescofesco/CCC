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
    do_run("example");
    // for i in 1..=5 {
    //     do_run(&i.to_string())
    // }
}

#[derive(Clone, Copy, Default, PartialEq, Eq)]
enum Field {
    #[default]
    None,
    X,
    WTF,
    Empty,
}

fn place_hori(grid : &mut grid::Grid<Field>, x : usize, y : usize) -> bool
{
    for dx in 0..3 {
        for dy in 0..2 {
            match grid.get(y + dy, x + dx) {
                Some(Field::None) => (),
                _ => {
                   return false;
                }
            }
        }
    }

    *grid.get_mut(y + 0, x + 0).unwrap() = Field::X;
    *grid.get_mut(y + 0, x + 1).unwrap() = Field::X;
    *grid.get_mut(y + 0, x + 2).unwrap() = Field::WTF;

    *grid.get_mut(y + 1, x + 0).unwrap() = Field::Empty;
    *grid.get_mut(y + 1, x + 1).unwrap() = Field::Empty;
    *grid.get_mut(y + 1, x + 2).unwrap() = Field::Empty;

    return true;
}

fn place_verti(grid : &mut grid::Grid<Field>, x : usize, y : usize) -> bool
{
    for dx in 0..2 {
        for dy in 0..3 {
            match grid.get(y + dy, x + dx) {
                Some(Field::None) => (),
                _ => {
                   return false;
                }
            }
        }
    }

    *grid.get_mut(y + 0, x + 0).unwrap() = Field::X;
    *grid.get_mut(y + 1, x + 0).unwrap() = Field::X;
    *grid.get_mut(y + 2, x + 0).unwrap() = Field::WTF;

    *grid.get_mut(y + 0, x + 1).unwrap() = Field::Empty;
    *grid.get_mut(y + 1, x + 1).unwrap() = Field::Empty;
    *grid.get_mut(y + 2, x + 1).unwrap() = Field::Empty;

    return true;
}

pub fn do_run(sublevel: &str) {
    let mut file = File::open(&format!("input/level5/level5_{sublevel}.in")).unwrap();
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
            x,
            y: token.next().unwrap().parse().unwrap(),
            desks: token.next().unwrap().parse().unwrap(),
        });
    }

    assert!(rooms.len() == room_count as usize);

    let mut outstring = String::new();
    for r in rooms {
        let mut grid: grid::Grid<Field> = grid::Grid::new((r.y + 1) as usize, (r.x + 1) as usize);
        let mut num_placed = 0;
        for x in 0..r.x {
            for y in 0..r.y {
                if *grid.get(y, x).unwrap() != Field::None {
                    continue;
                }

               

                if place_hori(&mut grid, x as usize, y as usize)
                {
                    num_placed += 1;
                    continue;
                }

                if place_verti(&mut grid, x as usize, y as usize)
                {
                    println!("jey");
                    num_placed += 1;
                    continue;
                }
            }
        }

        // assert_eq!(num_placed, r.desks);

        {
            for x in 0..r.x {
                for y in 0..r.x {
                    match grid.get(y, x) {
                        Some(Field::X) => outstring.push('x'),
                        Some(Field::None) => outstring.push('?'),
                        Some(Field::WTF) => outstring.push('W'),
                        
                        _ => outstring.push('.'),
                    }
                }
                outstring.push('\n');
            }
        }
        outstring.push('\n');
    }

    let mut outfile = File::create(&format!("output/level5/level5_{sublevel}.out")).unwrap();

    outfile.write_all(outstring.as_bytes()).unwrap();
}
