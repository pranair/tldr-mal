from flask import Flask, jsonify, request, send_from_directory
from app import malsum

app = Flask(__name__,
            static_folder="./static/",
            static_url_path='',
            template_folder="./static")

@app.route("/", defaults={'path': 'index.html'})
def index(path):
    return send_from_directory('static', path)

@app.route("/docs", defaults={'path': 'docs.html'})
def docs(path):
    return send_from_directory('static', path)


@app.route("/about", defaults={'path': 'about.html'})
def about(path):
    return send_from_directory('static', path)

@app.route("/api/summarize", methods=['POST', 'GET'])
def do_summarize():
    result = {}
    text = ""
    length = 0
    if request.method == 'POST':
        text = request.form['source']
        length = request.form['length']
    return jsonify(malsum.summarize(text, int(length)))
    return None


if __name__ == "__main__":
    app.run()
