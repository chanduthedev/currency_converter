from flask import Flask, request, send_from_directory, render_template, jsonify
import json

with open("config.json", 'r') as f:
    datastore = json.load(f)

app = Flask(__name__, template_folder='.')


@app.route("/")
def hello():
    return render_template("default.html")


@app.route("/convert", methods=["GET", "POST", "PUT"])
def convert_api():
    # ToDo : add code to complete the logic
    pass
    return jsonify({"message": "1.0000"}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=900)
