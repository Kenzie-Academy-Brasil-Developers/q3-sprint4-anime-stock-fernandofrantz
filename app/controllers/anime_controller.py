from http import HTTPStatus
import http
from multiprocessing.context import set_spawning_popen
from platform import release

from flask import jsonify, request
from app.models.anime_model import Anime
from app.models import conn

# create anime
def create_anime():
    anime_request = request.get_json()
    cur = conn.cursor()
    formated_name = ''
    name = anime_request.get('anime')
    released = anime_request.get('released_date')
    seasons = anime_request.get('seasons')

    create_table = f"""
    CREATE TABLE IF NOT EXISTS animes(
        id BIGSERIAL PRIMARY KEY,
        anime VARCHAR(100) NOT NULL UNIQUE,
        released_date DATE NOT NULL,
        seasons INTEGER NOT NULL
    )"""

    cur.execute(create_table)
    conn.commit()

    if (name == None or released == None or seasons == None):
        return jsonify(
            {
                "available_keys": [
                    "anime",
                    "released_date",
                    "seasons"
                ]
            }
        ), HTTPStatus.UNPROCESSABLE_ENTITY

    for word in anime_request.get('anime').split(' '):
        if(len(formated_name) < len(anime_request.get('anime').split(' ')) -1):
            formated_name  += word.capitalize() + ' '
        else:
            formated_name  += word.capitalize()

    query_to_get_animes = "SELECT * FROM animes;"
    cur.execute(query_to_get_animes)
    animes = cur.fetchall()
    for anime_details in animes:
        if (anime_details[1] == formated_name):
            return jsonify({"error": "anime already exists"})

    values = (
        formated_name,
        released,
        seasons
    )

    query_to_create_animes = f"""
    INSERT INTO animes(anime, released_date, seasons) VALUES {values} RETURNING *;
    """

    cur.execute(query_to_create_animes)
    conn.commit()
    created_anime = cur.fetchall()

    anime_keys = ['seasons', 'anime', 'released_date']
    animes_list = [dict(zip(anime_keys, ani)) for ani in created_anime]
    return jsonify(animes_list), HTTPStatus.CREATED

# get animes\
def get_animes():
    cur = conn.cursor()
    create_table = f"""
    CREATE TABLE IF NOT EXISTS animes(
        id BIGSERIAL PRIMARY KEY,
        anime VARCHAR(100) NOT NULL UNIQUE,
        released_date DATE NOT NULL,
        seasons INTEGER NOT NULL
    )"""
    cur.execute(create_table)
    conn.commit()
    cur.close()

    cur = conn.cursor()
    query_to_get_animes = "SELECT * FROM animes;"
    cur.execute(query_to_get_animes)
    animes = cur.fetchall()

    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, ani)) for ani in animes]

    return {"data": (animes_list)}, HTTPStatus.OK

# get anime por id
def get_anime_by_id(anime_id):

    query_to_get_animes = "SELECT * FROM animes;"
    cur = conn.cursor()
    cur.execute(query_to_get_animes)
    animes = cur.fetchall()
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, ani)) for ani in animes]

    for anime in animes_list:
        if (anime['id'] == anime_id):
            return {"data": [(anime)]}, HTTPStatus.OK

    return {'error': 'not found'}, HTTPStatus.NOT_FOUND

# update anime
def update_anime(anime_id):

    request_update_data = request.get_json()

    formated_name = ''
    name = request_update_data.get('anime')
    released = request_update_data.get('released_date')
    seasons = request_update_data.get('seasons')

    if (name == None and released == None and seasons == None):
            return jsonify(
                {
                    "available_keys": [
                        "anime",
                        "released_date",
                        "seasons"
                    ]
                }
        ), HTTPStatus.UNPROCESSABLE_ENTITY

    if (name != None):
        for word in request_update_data.get('anime').split(' '):
            if(len(formated_name) < len(request_update_data.get('anime').split(' ')) -1):
                formated_name  += word.capitalize() + ' '
            else:
                formated_name  += word.capitalize()
        
        query_to_update = f"update animes set anime='{formated_name}' where id={anime_id};;"
        cur = conn.cursor()
        cur.execute(query_to_update)
        conn.commit()
        cur.close()
    
    if (released != None):
        query_to_update = f"update animes set released_date='{released}' where id={anime_id};;"
        cur = conn.cursor()
        cur.execute(query_to_update)
        conn.commit()
        cur.close()
    
    if (seasons != None):
        query_to_update = f"update animes set seasons='{seasons}' where id={anime_id};;"
        cur = conn.cursor()
        cur.execute(query_to_update)
        conn.commit()
        cur.close()

    query_to_get_animes = "SELECT * FROM animes;"
    cur = conn.cursor()
    cur.execute(query_to_get_animes)
    animes = cur.fetchall()
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, ani)) for ani in animes]

    for anime in animes_list:
        if (anime['id'] == anime_id):
            return {"data": [(anime)]}, HTTPStatus.OK

    return {"error": "not found"}, HTTPStatus.NOT_FOUND

# delete anime
def delete_anime(anime_id):
    query_to_get_animes = "SELECT * FROM animes;"
    cur = conn.cursor()
    cur.execute(query_to_get_animes)
    animes = cur.fetchall()
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, ani)) for ani in animes]

    for anime in animes_list:
        if (anime['id'] == anime_id):
            query_to_delete_anime = f"DELETE FROM animes WHERE id={anime_id} RETURNING *;"
            cur = conn.cursor()
            cur.execute(query_to_delete_anime)
            conn.commit()
            cur.close()
            return '', HTTPStatus.NO_CONTENT
    return {'error': 'not found'}, HTTPStatus.NOT_FOUND