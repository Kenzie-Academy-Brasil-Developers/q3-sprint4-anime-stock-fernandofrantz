from flask import Flask, Blueprint, request
from app.controllers import anime_controller

bp = Blueprint('animes', __name__, url_prefix='/api')

# criação de animes
@bp.post('/animes')
def create_anime():
    return anime_controller.create_anime()

# obtenção dos animes
@bp.get('/animes')
def get_animes():
    return anime_controller.get_animes()

# obtenção de um anime por id
@bp.get('/animes/<int:anime_id>')
def get_anime_by_id(anime_id):
    return anime_controller.get_anime_by_id(anime_id)

# update de um anime
@bp.patch('/animes/<int:anime_id>')
def update_anime(anime_id):
    return anime_controller.update_anime(anime_id)

# deletar anime
@bp.delete('/animes/<int:anime_id>')
def delete_anime(anime_id):
    return anime_controller.delete_anime(anime_id)