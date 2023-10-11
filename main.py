from flask import Flask, jsonify, request, render_template
import subprocess
import random
import string
import yaml
import json
import os

app = Flask(__name__)

with open('settings.yml') as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

@app.route('/')
def home():
    return render_template('index.html', code='', output='', error='')

@app.route('/<name>')
def home_share(name: str):
    if name != 'favicon.ico':
        with open(f'shares/{name}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            f.close
        return render_template('index.html', code=data['code'], output=data['output'], error=data['error'])
    else:
        return ''

@app.route('/api/execute', methods=['POST'])
def execute_code():
    code = request.json['code']
    
    if any(i in code for i in settings['black-list']):
        return jsonify({
            'output': "",
            'error': settings['black-list-message']
        })
    
    try:
        result = subprocess.run(['python'], input="# -*- coding: utf-8 -*-\n"+code, capture_output=True, text=True, timeout=settings['timeout'], encoding='utf-8')
        
        output = result.stdout
        error = result.stderr
        
        return jsonify({
            'output': output,
            'error': error
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'output': "",
            'error': settings['timeout-message']
        })

@app.route('/api/share', methods=['POST'])
def share():
    code = request.form['code']
    output = request.form['output']
    error = request.form['error']

    if not os.path.exists('shares'):
        os.makedirs('shares')
        
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    while os.path.exists(os.path.join('shares', random_string + '.json')):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    data = {
        'code': code,
        'output': output,
        'error': error
    }
    with open(os.path.join('shares', random_string + '.json'), 'w') as f:
        json.dump(data, f)

    url = f"{settings['url']}/{random_string}"

    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(host=settings['host'], port=settings['port'])