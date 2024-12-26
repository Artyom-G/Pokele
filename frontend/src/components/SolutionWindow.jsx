import React, { useState } from "react";
import './SolutionWindow.css';

const PokemonWindow = ({pokemon}) => {

    return(
        <>
            <div className="pokemon-solution-container">
                <div className="row">
                    <span className="pokemon-solution-id gray-text">#{pokemon.id}</span>
                    <span className="pokemon-solution-name">{pokemon.name}</span>
                    <span className="pokemon-solution-gen">Gen {pokemon.gen}</span>
                </div>

                <div className="pokemon-solution-row-2">
                    <div className="pokemon-solution-types">
                        <span>Types: </span>
                        {pokemon.types.map((type, index) => (
                            <span key={index} className="pokemon-solution-type-item">{type}</span>
                        ))}
                    </div>
                    <div className="pokemon-solution-picture-border-border" style={{ border: `solid ${pokemon.primary_color} 4px` }}>
                        <div className="pokemon-solution-picture-border" style={{ border: `solid ${pokemon.secondary_color} 2px` }}>
                            <img
                                className="pokemon-solution-picture"
                                src={pokemon.picture}
                                alt={pokemon.name}
                            />
                        </div>
                    </div>
                    <div className="pokemon-solution-abilities">
                        <span>Abilities: </span>
                        {pokemon.abilities.map((ability, index) => (
                            <span key={index} className="pokemon-solution-ability-item">{ability}</span>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}

export default PokemonWindow;
