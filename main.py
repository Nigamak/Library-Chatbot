import json
import zlib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to compress data
def compress_data(data):
    json_str = json.dumps(data)
    compressed = zlib.compress(json_str.encode('utf-8'))
    return compressed

# Function to decompress data
def decompress_data(compressed_data):
    decompressed = zlib.decompress(compressed_data).decode('utf-8')
    data = json.loads(decompressed)
    return data

# Load and compress catalogs and policies
with open('catalogs.json', 'r') as f:
    catalogs = json.load(f)
compressed_catalogs = compress_data(catalogs)

with open('policies.json', 'r') as f:
    policies = json.load(f)
compressed_policies = compress_data(policies)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_books', methods=['POST'])
def search_books():
    query = request.form.get('query', '').lower()
    catalogs_data = decompress_data(compressed_catalogs)
    results = [book for book in catalogs_data['books'] if query in book['title'].lower() or query in book['author'].lower()]
    return render_template('results.html', results=results, query=query)

@app.route('/policies')
def get_policies():
    policies_data = decompress_data(compressed_policies)
    return render_template('policies.html', policies=policies_data['borrowing_policies'])

if __name__ == '__main__':
    app.run(debug=True)
