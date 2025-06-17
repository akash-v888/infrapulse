from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "status": "OK",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "message": "Welcome to InfraPulse! The app is running."
    })

@app.route("/health")
def health_check():
    return jsonify({"health": "pass", "service": "InfraPulse Flask API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
