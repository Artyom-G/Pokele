import { useState } from 'react'
import GuessField from './components/GuessField'
import SolutionWindow from './components/SolutionWindow'
import PokemonWindow from './components/PokemonWindow'
import './App.css'

function App() {

    const [pokemonSolution, setPokemonSolution] = useState({
        id: "????",
        name: "???",
        abilities: [],
        color: "#ffffff50",
        gen: "???",
        picture: "https://static.wikia.nocookie.net/bec6f033-936d-48c5-9c1e-7fb7207e28af/scale-to-width/755",
        types: [],
    })

    const [pokemonGuess, setPokemonGuess] = useState(pokemonSolution)

    const makeGuess = (guess, validatedGuess) => {
        // Combine known information
        var id = ""
        for (let i = 0; i < pokemonSolution.id.length; i++) {
            if(pokemonSolution.id[i] !== "?"){
                id += pokemonSolution.id[i]
            }
            else if(validatedGuess.id){
                id += validatedGuess.id[i]
            }
            else{
                id += "?"
            }
        }

        setPokemonSolution((prevPokemon) => ({
            id: id || prevPokemon.id,
            name: validatedGuess.name || prevPokemon.name,
            abilities: validatedGuess.abilities
                ? [...new Set([...prevPokemon.abilities, ...validatedGuess.abilities])]
                : prevPokemon.abilities,
            color: validatedGuess.color || prevPokemon.color,
            primary_color: validatedGuess.primary_color || prevPokemon.primary_color,
            secondary_color: validatedGuess.secondary_color || prevPokemon.secondary_color,
            gen: validatedGuess.gen || prevPokemon.gen,
            picture: validatedGuess.picture || prevPokemon.picture,
            types: validatedGuess.types
                ? [...new Set([...prevPokemon.types, ...validatedGuess.types])]
                : prevPokemon.types,
        }));
        setPokemonGuess(guess);
    };

    return (
        <>
            <div className='body'>
                <SolutionWindow pokemon={pokemonSolution}/>
                <PokemonWindow pokemon={pokemonGuess}/>
                <GuessField makeGuess={makeGuess}/>
            </div>
            <div className='background'/>
            <span className='logo'>Pokéle</span>
        </>
    )
}

export default App
