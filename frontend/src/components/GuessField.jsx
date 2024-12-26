import React, { useState } from "react";
import "./GuessField.css";

const GuessField = ({ makeGuess }) => {

    const [guess, setGuess] = useState("")
    const [guesses, setGuesses] = useState([])

    const onSubmit = async (e) => {
        if (guess && !(guess in guesses)) {
            e.preventDefault()

            const url = `http://127.0.0.1:5000/api/v1/guess/${guess}`
            const options = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
            const response = await fetch(url, options)
            if (response.status !== 201 && response.status !== 200) {
                const data = await response.json()
                console.log(`Pokemon ${guess} does not exist!\n${data.message}`)
                alert(`Pokemon ${guess} does not exist!`)
            }
            else {
                const data = await response.json()
                console.log(data.response)
                
                const guessUrl = `http://127.0.0.1:5000/api/v1/${guess}`
                const guessOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
                const guessResponse = await fetch(guessUrl, guessOptions)
                if (guessResponse.status !== 201 && guessResponse.status !== 200) {
                    const guessData = await guessResponse.json()
                    console.log(`Pokemon ${guess} does not exist!\n${guessData.message}`)
                }
                else {
                    const guessData = await guessResponse.json()
                    console.log(guessData.pokemon)
                    setGuesses([...guesses, guessData.pokemon])
                    makeGuess(guessData.pokemon, data.response)
                }
            }
        }
    }

    return (
        <>
            <form className="guess-form" onSubmit={onSubmit}>
                <input
                    type="text"
                    id="guess"
                    value={guess}
                    onChange={(e) => setGuess(e.target.value)}
                    className="guess-input"
                />
            </form>

            <div className="guess-items">
                {guesses.reverse().map((guess, key) => {
                    return(
                        <div className="guess-item" key={key}>
                            <div className="guess-ids">
                                <span className="guess-id gray-text">#{guess.id}</span>
                                <span className="guess-name">{guess.name}</span>
                            </div>
                            <img className="guess_pokemon_picture" src={guess.picture} alt={guess.name} />
                        </div>
                    );
                })}
            </div>
        </>
    );
}

export default GuessField;

