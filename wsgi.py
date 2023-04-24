import os
import sys

# Add the parent directory of this file to the sys.path to make sibling packages importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'swagger_server')))

# Import the app module from the all_methods.swagger_server.test package
from swagger_server.test import BaseTestCase
app = BaseTestCase().create_app()

if __name__ == "__main__":
    # Start the Flask development server
    app.run()

