fn main() {
    let mut text = String::from("Hello");
    println!("Antes: {text}");
    append(&mut text);
    println!("Depois: {text}");
}

fn append(value: &mut String) {
    value.push_str(" world!");
}
