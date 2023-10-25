from flask import Flask, jsonify, request, render_template, redirect
import subprocess
import requests
import random
import string
import yaml
import json
import os

app = Flask(__name__)

with open('settings.yml') as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

if settings['short-link']:
    if settings['goo.su']['environ']:
        settings['goo.su']['goo.su-apikey'] = os.environ['GOO_SU_APIKEY']
    if settings['my']['environ']:
        settings['my']['headers'] = os.environ['MY_HEADERS']

if not os.path.exists('shares'):
    os.makedirs('shares')

@app.route('/')
@app.route('/<name>')
def home(name: str = ''):
    if name == 'favicon.ico':
        return redirect("/static/img/favicon.png")
    
    if name:
        try:
            with open(f'shares/{name}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return redirect("/")
    
        return render_template('index.html', code=data['code'], output=data['output'], error=data['error'])
        
    return render_template('index.html', code='', output='', error='')

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

    if settings['short-link']:
        if settings['short-link-service'] == "goo.su":
            headers_gooso = {
                'content-type': 'application/json',
                'x-goo-api-token': settings['goo.su-apikey']
            }
            data_gooso = {
                'url': f"{settings['url']}/{random_string}",
                'is_public': False,
                'group_id': 2
            }
            try:
                response = requests.post('https://goo.su/api/links/create', headers=headers_gooso, json=data_gooso)
                url = response.json()['short_url']
            except:
                url = f"{settings['url']}/{random_string}"
        elif settings['short-link-service'] == "my":
            data_my_sl = {settings['my']['data-url']: f"{settings['url']}/{random_string}"}
            
            try:
                response = requests.post(settings['my']['url'], headers=eval(settings['my']['headers']), json=data_my_sl)
                url = response.json()[settings['my']['response']]
            except:
                url = f"{settings['url']}/{random_string}"
        else:
            url = f"{settings['url']}/{random_string}"
    else:
        url = f"{settings['url']}/{random_string}"

    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(host=settings['host'], port=settings['port'])