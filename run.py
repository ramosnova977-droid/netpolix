from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from app.routes.video_routes import video_bp
from app.routes.cliente_routes import cliente_bp
from app.routes.venta_routes import venta_bp
from app.routes.calificacion_routes import calificacion_bp
from app.routes.gerente_routes import gerente_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(venta_bp)
app.register_blueprint(calificacion_bp)
app.register_blueprint(video_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(gerente_bp)

@app.route("/")
def home():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "netpolix.html")

@app.route("/admin")
def admin():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "admin.html")

if __name__ == "__main__":
    app.run(debug=True)