"""CRUD operations."""

from model import db, StateData, connect_to_db

def get_data_by_year(data_year):
    """returns year from year chosen from dropdown"""
    return StateData.query.filter(State.data_year).all()


def get_data_by_state_and_year(state):
    """gets state from map click by state id"""
    pass

def create_state_PIT_data(state, count, year):
    """create and return an entry of state Point in Time count for a state"""
    pit_count = StateData(state=state_id,
                          count=count,
                          year=data_year)
    
    db.session.add(pit_count)
    db.session.commit()

    return pit_count
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)