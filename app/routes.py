from app import app
from app.utils.parser import Parser
from app.utils.search import Search
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
        output.update(search)

    return jsonify(output)