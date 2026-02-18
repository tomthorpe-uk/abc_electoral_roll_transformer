import pandas as pd

def monthly_update_to_full_file(data: pd.DataFrame) ->pd.DataFrame:
    output_df = pd.DataFrame(index=data.index)

    # deconstruct the ElectorNumber and assign to 3 columns in output
    split_raw = data["ElectorNumber"].str.split(r'[-/]', expand=True)
    split_elector_number = split_raw.reindex(columns=range(3))    
    split_elector_number.columns = ["Elector Number Prefix", "Elector Number", "Elector Number Suffix"]
    split_elector_number["Elector Number Suffix"] = split_elector_number["Elector Number Suffix"].fillna(0)

    # create address 6 if required for long addresses
    address_6 = pd.Series(None, index=data.index, dtype="object")
    address_6_required =(~data["PropertyAddress5"].isnull()) & (data["PropertyAddress5"] != data["PropertyPostCode"])
    address_6.loc[address_6_required] = data["PropertyPostCode"]

    # mapping to new df
    output_df["Elector Number Prefix"] = split_elector_number["Elector Number Prefix"]
    output_df["Elector Number"] = split_elector_number["Elector Number"]
    output_df["Elector Number Suffix"] = split_elector_number["Elector Number Suffix"]
    output_df["Elector Markers"] = data["MarkersRegisterText"]
    output_df["Elector DOB"] = data["ElectorDOB"]
    output_df["Elector Surname"] = data["ElectorSurname"]
    output_df["Elector Forename"] = data["ElectorForename"]
    output_df["Address1"] = data["PropertyAddress1"]
    output_df["Address2"] = data["PropertyAddress2"]
    output_df["Address3"] = data["PropertyAddress3"]
    output_df["Address4"] = data["PropertyAddress4"]
    output_df["Address5"] = data["PropertyAddress5"]
    output_df["Address6"] = address_6
    output_df["PostCode"] = data["PropertyPostCode"]
    output_df["Elector ID"] = data["ElectorNumber"]
    
    return output_df