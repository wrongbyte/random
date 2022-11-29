struct Rectangle {
    length: u32,
    width: u32,
}

fn main() {
    let rect1 = Rectangle { length: 50, width: 30 };

    println!("The area is: {}", area(&rect1) )
}

fn area(rect: &Rectangle) -> u32 {
    rect.length * rect.width
}