from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

app = Flask(__name__, template_folder='frontend', static_folder='frontend')
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/search')
def search_program():
    program_name = request.args.get('program', '').strip()
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 3))
    
    if not program_name:
        return jsonify({'error': 'Please provide a program name'}), 400
    
    try:
        with open("scraper/scraped_requirements.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        search_term = program_name.lower().replace(' ', '').replace('-', '')
        
        matches = []
        for program in data:
            program_normalized = program['program_name'].lower().replace('-', '').replace(' ', '')
            
            if search_term in program_normalized:
                matches.append(program)
        
        if matches:
            start = offset
            end = offset + limit
            page_results = matches[start:end]
            
            return jsonify({
                'programs': page_results,
                'total': len(matches),
                'offset': offset,
                'limit': limit,
                'has_more': end < len(matches)
            })
        else:
            return jsonify({'error': f'No programs found matching "{program_name}"'}), 404
            
    except FileNotFoundError:
        return jsonify({'error': 'Requirements file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 500

@app.route('/api/program/<program_name>')
def get_specific_program(program_name):
    try:
        with open("scraper/scraped_requirements.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        program = next((p for p in data if p['program_name'].lower() == program_name.lower().replace(' ', '-')), None)
        
        if program:
            return jsonify(program)
        else:
            return jsonify({'error': f'Program "{program_name}" not found'}), 404
            
    except FileNotFoundError:
        return jsonify({'error': 'Requirements file not found'}), 500