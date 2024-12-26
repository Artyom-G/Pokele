import React, { useState } from "react";

const GuessField = () => {

    const [pokemon, setPokemon] = useState("")

    const onSubmit = async (e) => {
        if(pokemon){
            e.preventDefault()

            const url = `http://127.0.0.1:5000/api/v1/guess/${pokemon}`
            const options = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
            const response = await fetch(url, options)
            if(response.status !== 201 && response.status !== 200){
                const data = await response.json()
                console.log(`Pokemon ${pokemon} does not exist!\n${data.message}`)
                //alert(`Pokemon ${pokemon} does not exist!`)
            }
            else{
                const data = await response.json()
                console.log(data)
            }
        }
    }

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="pokemon">Pokemon</label>
                <input
                    type="text"
                    id="pokemon"
                    value={pokemon}
                    onChange={(e) => setPokemon(e.target.value)}
                />
            </div>
            <button type="submit">Submit Guess</button>
        </form>
    );
}

export default GuessField;

