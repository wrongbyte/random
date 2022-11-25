fn main() {
    let mut numero = 3;

    if numero < 5 {
        println!("true");
    } else {
        println!("false");
    }

    while numero != 0 {
        println!("{}!", numero);

        numero = numero - 1;
    }

    println!("LIFTOFF!!!");
    let a = [10, 20, 30, 40, 50];

    for elemento in a.iter() {
        println!("O valor é: {}", elemento);
    }

    for i in (1..4).rev() {
        println!("counting... {}", i);
    }

}
