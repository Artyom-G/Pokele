import React, { useState } from "react";
import './SolutionWindow.css';

const PokemonWindow = ({pokemon}) => {

    return(
        <>
            <div className="pokemon-solution-container">
                <div className="row">
                    <span className="pokemon-solution-id gray-text">#{pokemon.id}</span>
                    <span className="pokemon-solution-name">{pokemon.name}</span>
                    <div className="pokemon-solution-types">
                        <span>Types: </span>
                        <ul className="column">
                            {pokemon.types.map((type, index) => (
                                <span key={index} className="pokemon-solution-type-item">{type}</span>
                            ))}
                        </ul>
                    </div>
                </div>

                <div className="row">
                    <span className="pokemon-solution-gen">Gen {pokemon.gen}</span>

                    <div className="pokemon-solution-abilities">
                        <span>Abilities: </span>
                        <ul className="column">
                            {pokemon.abilities.map((ability, index) => (
                                <span key={index} className="pokemon-solution-ability-item">{ability}</span>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </>
    );
}

export default PokemonWindow;
