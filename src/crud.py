import pandas as pd


def apply_create(data: pd.DataFrame, updates: pd.DataFrame):
    return pd.concat([data, updates], ignore_index=True)

def apply_edits(data: pd.DataFrame, updates: pd.DataFrame):
    data_by_id = data.set_index("Elector ID")
    updates_by_id = updates.set_index("Elector ID")
    return updates_by_id.combine_first(data_by_id).reset_index()

def apply_deletes(data: pd.DataFrame, updates: pd.DataFrame):
    return data[~data["Elector ID"].isin(updates["Elector ID"])]