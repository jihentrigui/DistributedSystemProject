from flask import Flask, request, jsonify
import requests
import random
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

duration = None ;

# Fonction pour diviser les données en plusieurs parties
def split_data(data, n):
    k, m = divmod(len(data), n)
    return [data[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

# Fonction pour fusionner plusieurs listes triées
def merge(*lists):
    result = []
    for lst in lists:
        result = sorted(result + lst)
    return result

# Envoyer une partie des données à trier à une machine distante
def send_to_machine(data_part, machine_url):
    response = requests.post(machine_url, json={'data': data_part})
    return response.json()

@app.route('/sort', methods=['POST'])
def sort_endpoint():
    try:
        # Retrieve the size of the array from the POST request
        n = int(request.get_json().get('n', 10))  # Default to 10 if not provided
        if n <= 0:
            raise ValueError("Array size must be a positive integer.")
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input for array size. Please provide a positive integer.'}), 400
    
    # Générer un tableau aléatoire
    data = [random.randint(0, 1000000) for _ in range(n)]
    
    # Diviser les données en 3 parties
    split_data_list = split_data(data, 3)

    # Adresses des machines distantes
    machine1_url = "http://192.168.1.33:5000/sort"
    machine2_url = "http://192.168.1.35:5000/sort"

    start = time.time()

    # Trier une partie localement
    sorted_part1 = sorted(split_data_list[0])

    # Envoyer les deux autres parties aux machines distantes
    sorted_part2 = send_to_machine(split_data_list[1], machine1_url)
    sorted_part3 = send_to_machine(split_data_list[2], machine2_url)

    # Fusionner les résultats triés
    final_sorted_data = merge(sorted_part1, sorted_part2, sorted_part3)
    

    duration = time.time() - start

    # Retourner les données triées et le temps d'exécution au frontend
    return jsonify({
        'sorted_data': final_sorted_data,
        'execution_time': duration
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
