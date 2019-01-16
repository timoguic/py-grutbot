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
    if not query:
        return "Error: empty string", 404

    return jsonify(
        Search(
            Parser(query).parse()
        ).search()
    )