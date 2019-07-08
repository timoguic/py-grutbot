from .app import app
from .utils import Parser, WikiSearch, Weather, Webcam, Geoloc
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')

@app.route('/api')
def api():
    query = request.args.get('query', None)

    parsed = Parser(query)
    if not parsed:
        output = {'parsed': False, 'message': 'Cannot parse query: {}'.format(query)}
    else:
        output = {}
        output['parsed'] = parsed

        coords = Geoloc(parsed)
        output['coords'] = coords

        search = WikiSearch(parsed, coords=coords)
        output['wiki'] = {'url': search.url, 'extract': search.extract}
        
        weather = Weather(coords)
        if weather:
            output['weather'] = weather
            
        webcam = Webcam(coords)
        if webcam:
            output['webcam'] = webcam

    return jsonify(output)