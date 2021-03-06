"""CRUD operations."""

from model import db, StateData, connect_to_db

def get_data_by_year(data_year):
    """returns year from year chosen from dropdown"""
    return StateData.query.filter(StateData.data_year == data_year).all()

# def get_total_population(data_year):
#     """returns total population from chosen year"""
#     allstates_for_year = StateData.query.filter(StateData.data_year == data_year).all()

#     return allstates_for_year.query(func.sum(StateData.state_population))


def get_data_by_state(state_name):
    """gets state from map click by state id"""
    return StateData.query.filter(StateData.state_name == state_name).all()

def create_state_data(state_id, state_name, data_year, pit_count, li_rental_inv=None, state_below_poverty=None, state_population=None):
    """create and return an entry of state Point in Time count for a state"""
    state_data = StateData(state_id=state_id,
                          state_name=state_name,
                          data_year=data_year,
                          pit_count=pit_count,
                          li_rental_inv=li_rental_inv,
                          state_below_poverty=state_below_poverty,
                          state_population=state_population)
    
    db.session.add(state_data)
    db.session.commit()

    return pit_count
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)