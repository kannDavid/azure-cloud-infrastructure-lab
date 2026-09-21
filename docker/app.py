from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Azure Cloud Lab</h1>
    <h2>Container is running successfully!</h2>

    <p>This app will later run in Azure.</p>

    <ul>
        <li>Framework: Flask</li>
        <li>Container: Docker</li>
        <li>Cloud target: Azure</li>
    </ul>
    """


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)