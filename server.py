from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# @app.route('/route_name')
# def method_name():
#    pass
@app.route('/state/ <data_year>)
def render_map(data_year):
    """gets year input from homepage and rerenders map"""
    
    all_states = crud.get_data_by_year(2019)
    
    return redirect('/', all_states=all_states)



# @app.route('/about')

#     """returns project about page"""
#     pass

# @app.route('/state')
#     """get state by state id"""
#     pass

