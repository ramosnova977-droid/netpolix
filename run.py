from flask import Flask
from flask_cors import CORS

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

@app.route('/')
def home():
    return {"message": "Backend funcionando"}

if __name__ == "__main__":
    app.run(debug=True)