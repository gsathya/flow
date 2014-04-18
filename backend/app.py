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

@app.route("/tracenow")
def tracenow():
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend'))
    return send_from_directory(path, "tracenow.html")

@app.route("/gettrace", methods=['GET'])
def gettrace():
    data = {}
    return jsonify(data)

@app.route("/monthly")
def monthly():
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'frontend'))
    return send_from_directory(path, "monthly.html")

@app.route("/monthlystatsformac", methods=['GET'])
def getmonthlystatsformac():
    mac = request.args.get('mac')
    data = db.getmonthlystatsformac(mac)
    return jsonify(data)

@app.route("/monthlystats", methods=['GET'])
def get():
    srcip = request.args.get('srcip')
    dstip = request.args.get('dstip')
    mac = request.args.get('mac')
    if dstip is None:
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
    
