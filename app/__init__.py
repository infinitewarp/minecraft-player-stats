from flask import Flask

app = Flask(__name__)

# Python linters will complain about the next line. It's OK! Ignore them.
from app import views
