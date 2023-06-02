from flask import Flask, render_template, session, request, redirect, jsonify, url_for
import json

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def root():
    return render_template("root.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)