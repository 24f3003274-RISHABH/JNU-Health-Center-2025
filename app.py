from flask import Flask
import os

# Load environment variables (optional - for local development)
try:
  from dotenv import load_dotenv
  load_dotenv()
except ImportError:
  pass

# for defining the database db in the app.py
from application.database import db #step3


app=None


def create_app():
  app=Flask(__name__)
  
  # Use environment variables with fallback defaults
  app.debug = os.getenv('FLASK_ENV', 'development') != 'production'
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', "sqlite:///hms.sqlite3") #step3
  app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
  
  db.init_app(app) #step3
  app.app_context().push()
  return app

app=create_app()

 
from application.controllers import *  # step2

# from application.models import *
if __name__=='__main__':
  #creating a unique admin details once then after i just commneted out 
  # db.create_all()
  # user1=User(name="admin" , email="admin8218@gmail.com",password="admin@8218", role="admin")
  # db.session.add(user1)
  # db.session.commit()


  app.run()
