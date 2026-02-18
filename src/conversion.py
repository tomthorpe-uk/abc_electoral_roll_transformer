import pandas as pd

def monthly_update_to_full_file(data: pd.DataFrame) ->pd.DataFrame:
    output_df = pd.DataFrame(columns=[
        "Elector Number Prefix",
        "Elector Number",
        "Elector Number Suffix",
        "Elector Markers",
        "Elector DOB",
        "Elector Surname",
        "Elector Forename",
        "PostCode",
        "Address1",
        "Address2",
        "Address3",
        "Address4",
        "Address5",
        "Address6",
        "Elector ID"
    ])

    # deconstruct the ElectorNumber
    output_df["Elector Number Prefix", "Elector Number", "Elector Number Suffix"] = data["ElectorNumber"].str.split(r"-/", expand=True)[0]
    output_df["Elector Number Suffix"].fillna(0)

    output_df["Elector Markers"] = data["MarkersRegisterText"]
    output_df["Elector DOB"] = data["ElectorDOB"]
    output_df["Elector Surname"] = data["ElectorSurname"]
    output_df["Elector Forename"] = data["ElectorForename"]
    output_df["Address1"] = data["PropertyAddress1"]
    output_df["Address2"] = data["PropertyAddress2"]
    output_df["Address3"] = data["PropertyAddress3"]
    output_df["Address4"] = data["PropertyAddress4"]
    output_df["Address5"] = data["PropertyAddress5"]

    # create address 6 if required for long addresses
    address_6_required =(~data["PropertyAddress5"].isnull()) & (data["PropertyAddress5"] != data["PropertyPostCode"])
    data["PropertyAddress6"] = None
    data.loc[address_6_required, "PropertyAddress6"] = data["PropertyPostCode"]
    output_df["Address6"] = data["PropertyAddress6"]

    output_df["Elector ID"] = data["ElectorNumber"]
    
    return output_df