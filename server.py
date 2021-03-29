from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app('/')
def render_map():
    """gets year input from homepage and rerenders map"""
    
    get_data_by_year()
    
    return redirect('/')



@app('/about')
    pass