import sys
import logging

# Add the path to your Flask application to sys.path
sys.path.insert(0, '/path/to/your/flask/app')

# Initialize logging to help with debugging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/path/to/venv/lib/python3.X/site-packages/")

from your_flask_app import app as application  # Import your Flask app instance

# Define the application for WSGI to serve
def application(environ, start_response):
    return application(environ, start_response)
