from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # templates 폴더에서 index.html을 렌더링
    return render_template("index.html")

if __name__ == "__main__":
    # Flask 서버 실행
    app.run(host="0.0.0.0", port=8080)

