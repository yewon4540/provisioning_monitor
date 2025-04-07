from flask import Flask, render_template
import pymysql
import os
from dotenv import load_dotenv
from db import get_router_status  # db.py에서 함수 가져옴

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    data = get_router_status()
    return render_template("status.html", routers=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # EC2에서 외부 접속 가능