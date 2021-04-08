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
    state_id, state_name, pit_count, data_year = (data['state_id'],
                                                  data['state_name'],
                                                  data['pit_count'],
                                                  data['data_year'])
    
    db_statedata = crud.create_state_data(state_id, state_name, pit_count, data_year)
    statedata_in_db.append(db_statedata)

