from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    with open(os.path.join(UPLOAD_FOLDER, "recording.raw"), "wb") as f:
        f.write(request.data)
    return "File received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)