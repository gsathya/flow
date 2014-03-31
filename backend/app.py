from flask import Flask, json, jsonify, request
import db

app = Flask(__name__)
    
@app.route("/", methods=['POST'])
def home():
    query = request.form['query']
    flag = request.form['type']
    data = db.process_db(query, flag)
    if(data == -1):
        return "Invalid request"
    return jsonify(data)

@app.route("/monthlystats", methods=['GET'])
def get():    
    srcip = request.args.get('srcip')
    dstip = request.args.get('dstip')
    data = db.getmonthlystats(srcip, dstip)
    result = jsonify(data)
    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
