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
    mac = request.args.get('mac')
    if mac is not None:
        data = db.getmonthlystatsformac(mac)
    elif dstip is None:
        data = db.getmonthlystats("122.107.200.10", "143.215.131.173")
    #TODO: need to implement
    #data = db.getmonthlystatsforsrcip(srcip)
    else:
        data = db.getmonthlystats(srcip, dstip)
    result = jsonify(data)
    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
