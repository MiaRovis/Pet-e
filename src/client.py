import httpx
import os

async def get_animals(
        api_key: str, 
        name: str,
        type: str,
        breed: str,
        size: str,
        gender: str,
        age: str,
        color: str,
        status: str,
)-> dict:
    api_key = os.environ.get('PETFINDER_API_KEY')
    url= f"https://api.petfinder.com/v2/animals"
    params = {
        "key": api_key,
        "name": name,
        "type": type,
        "breed": breed,
        "size": size,
        "gender": gender,
        "age": age,
        "color": color,
        "status": status
        }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()
    return response.json()


async def get_animal(api_key: str, id: str) -> dict:
    api_key = os.environ.get('PETFINDER_API_KEY')
    url= f"https://api.petfinder.com/v2/animals({id})"
    params = {"key": api_key, "animal_id": id}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()
    return response.json()


async def get_animal_types(api_key: str) -> dict:
    api_key = os.environ.get('PETFINDER_API_KEY')
    url= f"https://api.petfinder.com/v2/types"
    params = {"key": api_key}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()
    return response.json()


async def get_single_animal_type(api_key: str, type: str) -> dict:
    api_key = os.environ.get('PETFINDER_API_KEY')
    url= f"https://api.petfinder.com/v2/types/{type}"
    params = {"key": api_key, "animal_type": type}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()
    return response.json()


async def get_animal_breeds(api_key: str, type: str) -> dict:
    api_key = os.environ.get('PETFINDER_API_KEY')
    url= f"https://api.petfinder.com/v2/types/{type}/breeds"
    params = {"key": api_key, "animal_type": type}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()
    return response.json()

