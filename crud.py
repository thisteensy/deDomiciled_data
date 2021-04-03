"""CRUD operations."""

from model import db, StateData, connect_to_db

def get_data_by_year(data_year):
    """returns year from year chosen from dropdown"""
    return StateData.query.filter(StateData.data_year == data_year).all()


def get_data_by_state_and_year(state_id):
    """gets state from map click by state id"""
    return StateData.query.filter(StateData.state_id == state_id, StateData.data_year == 2019).one()

def create_state_pit_data(state_id, state_name, pit_count, data_year):
    """create and return an entry of state Point in Time count for a state"""
    state_data = StateData(state_id=state_id,
                          state_name=state_name,
                          pit_count=pit_count,
                          data_year=data_year)
    
    db.session.add(state_data)
    db.session.commit()

    return pit_count
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)