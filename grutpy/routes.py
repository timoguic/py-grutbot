from . import app
from .utils import Parser, Search, Weather, Webcam
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')


@app.route('/api')
def api():
    query = request.args.get('query', None)

    parsed = Parser(query)
    output = {'parsed': parsed}
    if not parsed:
        output.update({'message': 'Cannot parse query: {}'.format(query)})
    else:
        search = Search(parsed).process()
        coords = search['coords']
        weather = Weather(coords)
        output.update(weather)
        webcam = Webcam(coords[0], coords[1])
        if webcam:
            output.update(webcam)
        output.update(search)

    return jsonify(output)