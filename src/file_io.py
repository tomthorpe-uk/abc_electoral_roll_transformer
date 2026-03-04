import pandas as pd

def import_full_electoral_role(path: str) ->pd.DataFrame:
    data = pd.read_csv(path)

    # construct primary key for matching
    data["Elector ID"] = data["Elector Number Prefix"].astype(str) + "-" + data["Elector Number"].astype(str)
    nonzero_suffixed = data["Elector Number Suffix"] != 0
    data.loc[nonzero_suffixed, "Elector ID"] = data["Elector ID"].astype(str) + "/" + data["Elector Number Suffix"].astype(str)

    # fix trailing whitespace in forename column
    data["Elector Forename"].str.strip() 
    data["Elector Forename"] = data["Elector Forename"].str.strip()
    
    return data

def import_electoral_role_update(path: str) ->pd.DataFrame:
    data = pd.read_csv(path)

    adds_filter = data["ElectorCreatedMonth"] > 0
    data_adds = data[adds_filter]
    print(f"{data_adds.shape[0]} electors to add")

    edits_filter = data["ElectorChangedMonth"] > 0
    data_edits = data[edits_filter]
    print(f"{data_edits.shape[0]} electors to edit")

    deletes_filter = data["ElectorDeletedMonth"] > 0
    data_deletes = data[deletes_filter]
    print(f"{data_deletes.shape[0]} electors to delete")

    return data_adds, data_edits, data_deletes