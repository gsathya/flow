from flask import Flask, json, jsonify, request, render_template, send_from_directory
import os
import db

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend'))
    return send_from_directory(path, "index.html")

@app.route("/css/<file>", methods=["GET"])
def get_css(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend', "css"))
    return send_from_directory(path, file)

@app.route("/js/<file>", methods=["GET"])
def get_js(file):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend', "js"))
    return send_from_directory(path, file)

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
        data = db.getmonthlystatsforsrcip(srcip)
    else:
        data = db.getmonthlystats(srcip, dstip)
    result = jsonify(data)
    return result

# Return a deduplicated set of src ips
@app.route("/monthlysrc")
def getmonthlysrc():
    data = db.getmonthlysrc()
    result = jsonify(data)
    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
