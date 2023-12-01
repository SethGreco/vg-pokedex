from fastapi import APIRouter, Request
from ..util.conversion import inches_to_feet
from ..models.schema import Pokemon
from typing import List


router = APIRouter(prefix="/pokedex")


"""
TODO: Error handling
"""   
@router.get("", summary="Get all pokemon", response_model=List[Pokemon])
async def retreive_all_pokemon(request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * 
                FROM pokemon
            """)
            results = await cur.fetchall()
            pokemon_list = [Pokemon(number=pokemon[0],
                                    name=pokemon[1], 
                                    species=pokemon[2], 
                                    height=inches_to_feet(pokemon[3]), 
                                    weight=pokemon[4], 
                                    description=pokemon[5], 
                                    area=pokemon[6]) for pokemon in results]
            return pokemon_list
        
        

"""
TODO: Error handling
"""       
@router.get("/{number}", summary="Get single pokemon by number", response_model=Pokemon)
async def retreive_pokemon_by_number(number:int , request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT * FROM pokemon WHERE number = %s""", (number,), prepare=True)
            results = await cur.fetchone()
            pokemon = Pokemon(number=results[0],
                                    name=results[1], 
                                    species=results[2], 
                                    height=inches_to_feet(results[3]), 
                                    weight=results[4], 
                                    description=results[5], 
                                    area=results[6])
            return pokemon
        

"""
TODO: Error handling, case sensetive?
"""
@router.get("/name/{name}", summary="Get single pokemon by name", response_model=Pokemon)
async def retreive_pokemon_by_name(name:str , request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT * FROM pokemon WHERE name = %s""", (name,), prepare=True)
            results = await cur.fetchone()
            pokemon = Pokemon(number=results[0],
                                    name=results[1], 
                                    species=results[2], 
                                    height=inches_to_feet(results[3]), 
                                    weight=results[4], 
                                    description=results[5], 
                                    area=results[6])
            return pokemon

