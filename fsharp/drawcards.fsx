let cards = [0..5]
let hand = []

let drawCard (tuple: int list * int list) = 
    let deck = fst tuple // lembre-se que fst é da forma fst()
    let draw = snd tuple
    let firstCard = deck.Head
    printfn "%i" firstCard

    let hand = 
        draw
        |> List.append [firstCard]
    
    (deck.Tail, hand)
    
let d, h = (cards, hand) |> drawCard |> drawCard
printfn "Deck: %A Hand: %A" d h