// TODO: add even numbers checking

// usamos options para definir se o numero pertence à "categoria"
let (|MultOf3|_|) i = if i % 3 = 0 then Some MultOf3 else None
let (|MultOf5|_|) i = if i % 5 = 0 then Some MultOf5 else None

let checkNumber i = 
    match i with
    | MultOf3 & MultOf5 -> printfn "fizzbuzz"
    | MultOf3 -> printfn "fizz"
    | MultOf5 -> printfn "buzz"
    | _ -> printfn "%i" i

// List.iter é tipo um forEach
[1..30] |> List.iter checkNumber