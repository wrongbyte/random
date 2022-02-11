// sql.execute retorna uma lista (faz um map)
type Equipment = {
    tool: string
    quantity: string
}

let lista1 = [
        {tool="bowl"; quantity="1"}
        {tool="medium frying pan"; quantity="1"}
    ]

let list2 = []

let equipamento = {tool="bowl"; quantity="1"}

// typechecking with match pattern (single entity)
// the box keyword will always return an object, whether the source is reference type (as in this case) or a value type, in which case it will "box" it.
match box equipamento with
| :? Equipment -> printfn "it is an equipment"
| _ -> printfn "it is another type"

// funcao lista1 does not work; type inference will detect that it is a list
let funcao (inputTeste: Equipment) =
    match box inputTeste with
    | :? Equipment -> printfn "it is an equipment"
    | _ -> printfn "it is another type"