from flask import Flask
from flask_cors import CORS

#importar blueprint
from app.routes.video_routes import video_bp


app = Flask(__name__)
CORS(app)

# 👇 registrar rutas
app.register_blueprint(video_bp)


@app.route('/')
def home():
    return {"message": "Backend funcionando"}


if __name__ == "__main__":
    app.run(debug=True)