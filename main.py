from dataclasses import dataclass, asdict
from typing import Union
import json
from fastapi import FastAPI, Path, HTTPException

with open('pokemons.json', 'r') as file:
    data = json.load(file)

liste_pokemons = {k+1: v for k, v in enumerate(data)}

#==========================================================#

#dataclass est un utilitaire qui simplifie la creation de class qui servent a stocker des donnees
"""
    - __init__() automatise l'initialisation de la class(creation du constructeur avec les donnee qu'on lui transmet)
    -__repr__() Pour l'affichage de la class avec un print
"""

@dataclass
class Pokemon:
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None

#==========================================================#

pok1 = Pokemon(1, "Tinde Pehe Calixte", [""], 10, 1, 5, 9, 89,9,0)


#==========================================================#

#initialisation de l'application fastAPI
app = FastAPI()

#recuperer le nombre totale de pokemon
@app.get('/totale-pokemon')
def get_totale_pokemon() -> dict:
    return {"total":len(liste_pokemons)}

#recuperer tous les pokemons
@app.get('/pokemons')
def get_all_pokemons()->list[Pokemon]:
    pokemons = []
    for i in liste_pokemons:
        pokemons.append(Pokemon(**liste_pokemons[i]))
    return pokemons

#recuperer un pokemon a partir de son id
@app.get('/pokemon/{id}')
def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    if id not in liste_pokemons:
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    return liste_pokemons[id]

#ajouter un pokemon
@app.post('/pokemon')
def post_pokemon(pokemon:Pokemon)->Pokemon:
    if pokemon.id in liste_pokemons:
        raise HTTPException(status_code=404, detail=f"Un pokemon avec l'id {pokemon.id} existe deja")
    liste_pokemons[pokemon.id] = asdict(pokemon)
    return pokemon

#modifier un pokemon
@app.put('pokemon/{id}')
def uodate_pokemon(pokemon: Pokemon, id:int = Path(ge=1)) -> Pokemon:
    if pokemon.id not in liste_pokemons:
        raise HTTPException(status_code =404, detail="Ce pokemon n'existe pas")
    liste_pokemons[id] = asdict(pokemon)
    return pokemon

#supprimer un pokemon
@app.delete('/pokemon/{id}')
def delete_pokemon(id:int= Path(ge=1)) -> Pokemon:
    if id not in liste_pokemons:
        raise HTTPException(status_code=404, detail="Aucun pokemon n'a ce id")
    pokemonDeleted = liste_pokemons[id]
    del liste_pokemons[id]
    return pokemonDeleted
