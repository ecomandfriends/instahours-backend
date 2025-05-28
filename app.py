from flask import Flask, jsonify
import instaloader
from collections import Counter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde otros dominios

@app.route("/analyze/<username>")
def analyze(username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        post_times = []
        for post in profile.get_posts():
            post_times.append(post.date_local.hour)
            if len(post_times) >= 30:
                break

        counter = Counter(post_times)
        labels = [f"{h}:00" for h in range(24)]
        values = [counter.get(h, 0) for h in range(24)]

        return jsonify({"labels": labels, "values": values})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run()
