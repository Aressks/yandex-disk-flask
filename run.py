from flask import Flask
from app.routes import setup_routes

def create_app():
    app = Flask(__name__)
    
    # Настройка маршрутов
    setup_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)