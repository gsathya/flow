from flask import Flask, json, jsonify
import db
import json

app = Flask(__name__)
    
@app.route("/")
def hello():
    with open("data.json") as fh:
        data = json.load(fh)

    return jsonify(data)

if __name__ == "__main__":
    #db.process_db()
    app.run(debug=True)
    
