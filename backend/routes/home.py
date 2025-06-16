from flask import Blueprint, jsonify
import os

home_bp = Blueprint('home', __name__)

SIMULATIONS_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'simulations')

def get_simulations_for_category(category_path):
    full_path = os.path.join(SIMULATIONS_BASE_PATH, category_path)
    simulations = []
    if os.path.exists(full_path) and os.path.isdir(full_path):
        for filename in os.listdir(full_path):
            if filename.endswith('.py') and filename != '__init__.py':
                simulations.append(filename.replace('.py', ''))
    return simulations

@home_bp.route('/')
def home_route():
    categories = [
        {"name": "Cinemática", "path": "cinematica"},
        {"name": "Colisiones", "path": "colisiones"},
        {"name": "Dinámica", "path": "dinamica"},
        {"name": "Energía", "path": "energia"},
        {"name": "Electricidad y Magnetismo", "path": "electricidad_y_magnetismo"},
        {"name": "Ondas", "path": "ondas"}
    ]

    response_simulations = []
    for category in categories:
        sims = get_simulations_for_category(category['path'])
        response_simulations.append({
            "name": category['name'],
            "path": f"/{category['path'].replace('_', '-')}",
            "simulations": sims
        })

    return jsonify({
        "message": "Bienvenido a la API de Simulador de Física. Aquí están las categorías y simulaciones disponibles:",
        "categories": response_simulations
    })