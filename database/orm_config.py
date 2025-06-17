# FOOD_APP/database/orm_config.py

import os
from flask_sqlalchemy import SQLAlchemy
from flask import g # Import g for request-context session management

# Initialize the Flask-SQLAlchemy instance.
# It will be initialized with the Flask app instance in app.py.
db = SQLAlchemy()

# --- IMPORTANT NOTE ON SESSION MANAGEMENT ---
# With Flask-SQLAlchemy, you often use db.session directly within a Flask request context.
# Flask-SQLAlchemy automatically handles session creation, closing, and binding to the current
# application/request context.
# The 'get_db_session' function below can still be used if you prefer a consistent pattern
# or for specific scenarios outside of request context where you need a session.
def get_db_session():
    """
    Provides a database session for use within a Flask request context.
    Uses Flask's 'g' object to ensure the session is bound to the current request.
    """
    # If db_session is not already in the 'g' object for the current request,
    # assign Flask-SQLAlchemy's managed session.
    if 'db_session' not in g:
        g.db_session = db.session
    return g.db_session