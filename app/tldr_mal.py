from flask import Flask, jsonify, request, send_from_directory
from app import malsum

app = Flask(__name__,
            static_folder="./static/",
            static_url_path='',
            template_folder="./static")

@app.route("/", defaults={'path': 'index.html'})
def index(path):
    return send_from_directory('static', path)

@app.route("/api/summarize", methods=['POST', 'GET'])
def do_summarize():
    result = {}
    if request.method == 'POST':
        text = request.form['params']
    return jsonify(malsum.summarize(text, 4))
    return None


if __name__ == "__main__":
    app.run()
