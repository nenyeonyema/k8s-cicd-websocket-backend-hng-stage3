from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World! From Chinenye Genevieve Onyema: This simple web app is deployed on Kubernetes Cluster using Jenkins CICD pipeline"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

