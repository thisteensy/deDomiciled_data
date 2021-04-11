"""Script to seed database."""

import os
import json

import crud
import model
import server

os.system('dropdb deDomiciled')
os.system('createdb deDomiciled')
model.connect_to_db(server.app)
model.db.create_all()

with open('data/deDomiciled.json') as f:
    statedata = json.loads(f.read())
statedata_in_db = []
for data in statedata:
    state_id, state_name, data_year, pit_count, li_rental_inv, state_below_poverty, state_population = (data['state_id'],
                                                                                                        data['state_name'],
                                                                                                        data['data_year'],
                                                                                                        data['pit_count'],
                                                                                                        data.get('li_rental_inv'),
                                                                                                        data.get('state_below_poverty'),
                                                                                                        data.get('state_population'))
    
    db_statedata = crud.create_state_data(state_id, state_name, data_year, pit_count, li_rental_inv, state_below_poverty, state_population)
    statedata_in_db.append(db_statedata)

