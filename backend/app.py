from flask import Flask
import db

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    #db.process_db()
    app = Flask(__name__)
    app.run(debug=True)
    
