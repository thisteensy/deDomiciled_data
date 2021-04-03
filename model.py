"""model for unDomiciled Data app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StateData(db.Model):
    """data by state and year for population, houseless population counts, 
    low income housing inventory and per capita public spending on mental health services"""

    __tablename__ = 'state_data'

    data_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    state_id = db.Column(db.String)
    state_name = db.Column(db.String)
    data_year = db.Column(db.Integer)
    pit_count = db.Column(db.Integer)
    li_rental_inv = db.Column(db.Integer)
    state_pc_mh_spending = db.Column(db.Integer)
    state_population = db.Column(db.Integer)

    def __repr__(self):
        return f'<data_id = {self.data_id} state_id={self.state_id} data_year={self.data_year}>'

def connect_to_db(flask_app, db_uri='postgresql:///deDomiciled', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app

    connect_to_db(app)