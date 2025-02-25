from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Jenkins CICD deployed on Kubernetes by Chinenye Genevieve Onyema"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

