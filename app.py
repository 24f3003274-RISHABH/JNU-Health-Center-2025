from flask import Flask, jsonify
import os
import sys
import traceback

# Load environment variables (optional - for local development)
try:
  from dotenv import load_dotenv
  load_dotenv()
except ImportError:
  pass

# Import database
from application.database import db

def create_app():
  app = Flask(__name__)
  
  # Configuration
  app.debug = os.getenv('FLASK_ENV', 'development') != 'production'
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', "sqlite:///hms.sqlite3")
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
  
  # Initialize database
  db.init_app(app)
  
  # Create tables
  with app.app_context():
    try:
      db.create_all()
    except Exception as e:
      print(f"Warning: Could not create tables: {e}")
  
  # Health check endpoint
  @app.route('/health', methods=['GET'])
  def health():
    return jsonify({"status": "ok", "message": "Server is running"}), 200
  
  # Error handler
  @app.errorhandler(500)
  def handle_500(e):
    return jsonify({
      "error": "Internal Server Error",
      "message": str(e),
      "type": type(e).__name__
    }), 500
  
  return app

try:
  app = create_app()
  
  # Import controllers after app is created
  with app.app_context():
    from application.controllers import *  # step2
    
except Exception as e:
  print(f"Error during app initialization: {e}", file=sys.stderr)
  traceback.print_exc()
  # Create a minimal app if controllers fail to import
  app = create_app()
  
  @app.route('/')
  def error_page():
    return jsonify({
      "error": "Application failed to initialize",
      "details": str(e)
    }), 500


if __name__=='__main__':
  app.run()

# from application.models import *
if __name__=='__main__':
  #creating a unique admin details once then after i just commneted out 
  # db.create_all()
  # user1=User(name="admin" , email="admin8218@gmail.com",password="admin@8218", role="admin")
  # db.session.add(user1)
  # db.session.commit()


  app.run()
