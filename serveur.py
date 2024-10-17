from flask import Flask, request, jsonify
import random
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# Global variable to store the last execution time
duration = None

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
    split_data_list = split_data(data, 3)  # Changed back to 3 for splitting

    start = time.time()

    # Trier chaque partie localement
    sorted_parts = [sorted(part) for part in split_data_list]

    # Fusionner les résultats triés
    final_sorted_data = merge(*sorted_parts)

    global duration
    duration = time.time() - start

    print(duration)

    # Retourner les données triées et le temps d'exécution au frontend
    return jsonify({
        'sorted_data': final_sorted_data,
        'execution_time': duration
    })

if __name__ == '__main__':
    app.run(host='10.200.40.93', port=5000)
    
