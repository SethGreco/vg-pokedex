from fastapi import APIRouter, Request
from ..models.schema import Title, PokemonShort
from typing import List


router = APIRouter(prefix="/title")



#TODO: Error handling 
@router.get("", summary="Get all game titles", response_model=List[Title])
async def retreive_game_titles(request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * 
                FROM title
            """)
            results = await cur.fetchall()
            game_list = [Title(id=title[0], pokemonGame=title[1]) for title in results]
            return game_list
        


#TODO: Error handling 
@router.get("/{title}", summary="Get all pokemon from title", response_model=List[PokemonShort])
async def retreive_game_titles(request: Request, title:str):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT p.number, p.name
                    FROM pokemon p
                    JOIN title_join tj ON p.number = tj.pokemon_id
                    JOIN title t ON tj.title_id = t.id
                    WHERE t.game_title = %s""", (title,), prepare=True)
            results = await cur.fetchall()
            pokemon_list = [PokemonShort(number=pokemon[0],
                                    name=pokemon[1]) for pokemon in results]
            return pokemon_list