import pandas as pd

def import_full_electoral_role(path: str) ->pd.DataFrame:
    data = pd.read_csv(path)

    data["Elector Forename"].str.strip() # fix trailing whitespace
    
    return data

def import_electoral_role_update(path: str) ->pd.DataFrame:
    data = pd.read_csv(path)

    adds_filter = data["ElectorCreatedMonth"] > 0
    data_adds = data[adds_filter]

    edits_filter = data["ElectorChangedMonth"] > 0
    data_edits = data[adds_filter]

    deletes_filter = data["ElectorDeletedMonth"] > 0
    data_deletes = data[adds_filter]

    return data_adds, data_edits, data_deletes