from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    student = os.environ.get("STUDENT_NAME", "Студент")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname("/app/data/visits.txt"), exist_ok=True)
    
    with open("/app/data/visits.txt", "a") as f:
        f.write(f"{student} посетил страницу: {now}\n")
        
    return f"<h1>Эх, {student}!</h1><p>Время: {now}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)