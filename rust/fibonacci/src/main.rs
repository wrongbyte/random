use std::io;

fn main() {
    let mut input = String::new();

    println!("Input the maximum number of fibonacci sequence:");

    io::stdin()
        .read_line(&mut input)
        .expect("An error occurred");

    let max_number : i32 = input.trim().parse().expect("Error: input is not an integer");

    println!("Total sum: {}", fibonacci(max_number))
}

fn fibonacci (number: i32) -> i32 {
    if number <= 1 {
        return number
    }
    return fibonacci(number - 1) + fibonacci(number - 2);
}