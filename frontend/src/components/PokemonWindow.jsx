import React, { useState } from "react";
import './PokemonWindow.css';

const PokemonWindow = ({pokemon}) => {

    return(
        <>
            <div className="pokemon-container">
                <div className="row">
                    <span className="pokemon-id gray-text">#{pokemon.id}</span>
                    <span className="pokemon-gen">Gen {pokemon.gen}</span>
                </div>

                <div className="pokemon-picture-border-border" style={{ border: `solid ${pokemon.primary_color} 10px` }}>
                    <div className="pokemon-picture-border" style={{ border: `solid ${pokemon.secondary_color} 4px` }}>
                        <img
                            className="pokemon-picture"
                            src={pokemon.picture}
                            alt={pokemon.name}
                        />
                    </div>
                </div>

                <span className="pokemon-name">{pokemon.name}</span>
                <div className="pokemon-row-2 row">
                    <div className="pokemon-types">
                        <span>Types: </span>
                        {pokemon.types.map((type, index) => (
                            <span key={index} className="pokemon-type-item">{type}</span>
                        ))}
                    </div>

                    <div className="pokemon-abilities">
                        <span>Abilities: </span>
                        {pokemon.abilities.map((ability, index) => (
                            <span key={index} className="pokemon-ability-item">{ability}</span>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}

export default PokemonWindow;
