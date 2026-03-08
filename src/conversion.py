import pandas as pd
from schemas import MonthlyUpdateCols, FullRegisterCols, TVVUploadCols

def monthly_update_to_full_file(data: pd.DataFrame) ->pd.DataFrame:
    output_df = pd.DataFrame(index=data.index)

    # deconstruct the ElectorNumber and assign to 3 columns in output
    split_raw = data[MonthlyUpdateCols.ELECTOR_NUMBER].str.split(r'[-/]', expand=True)
    split_elector_number = split_raw.reindex(columns=range(3))    
    split_elector_number.columns = [FullRegisterCols.PREFIX, FullRegisterCols.NUMBER, FullRegisterCols.SUFFIX]
    split_elector_number[FullRegisterCols.SUFFIX] = split_elector_number[FullRegisterCols.SUFFIX].fillna(0)

    # create address 6 if required for long addresses
    address_6 = pd.Series(None, index=data.index, dtype="object")
    address_6_required =(~data[MonthlyUpdateCols.ADDRESS_5].isnull()) & (data[MonthlyUpdateCols.ADDRESS_5] != data[MonthlyUpdateCols.POSTCODE])
    address_6.loc[address_6_required] = data[MonthlyUpdateCols.POSTCODE]

    # mapping to new df
    output_df[FullRegisterCols.PREFIX] = split_elector_number[FullRegisterCols.PREFIX]
    output_df[FullRegisterCols.NUMBER] = split_elector_number[FullRegisterCols.NUMBER]
    output_df[FullRegisterCols.SUFFIX] = split_elector_number[FullRegisterCols.SUFFIX]
    output_df[FullRegisterCols.MARKERS] = data[MonthlyUpdateCols.MARKERS]
    output_df[FullRegisterCols.DOB] = data[MonthlyUpdateCols.ELECTOR_DOB]
    output_df[FullRegisterCols.SURNAME] = data[MonthlyUpdateCols.ELECTOR_SURNAME]
    output_df[FullRegisterCols.FORENAME] = data[MonthlyUpdateCols.ELECTOR_FORENAME]
    output_df[FullRegisterCols.ADDRESS_1] = data[MonthlyUpdateCols.ADDRESS_1]
    output_df[FullRegisterCols.ADDRESS_2] = data[MonthlyUpdateCols.ADDRESS_2]
    output_df[FullRegisterCols.ADDRESS_3] = data[MonthlyUpdateCols.ADDRESS_3]
    output_df[FullRegisterCols.ADDRESS_4] = data[MonthlyUpdateCols.ADDRESS_4]
    output_df[FullRegisterCols.ADDRESS_5] = data[MonthlyUpdateCols.ADDRESS_5]
    output_df[FullRegisterCols.ADDRESS_6] = address_6
    output_df[FullRegisterCols.POSTCODE] = data[MonthlyUpdateCols.POSTCODE]
    output_df[FullRegisterCols.ELECTOR_ID] = data[MonthlyUpdateCols.ELECTOR_NUMBER]
    
    return output_df

def full_file_to_tvv_upload(data: pd.DataFrame):
    output_df = pd.DataFrame(index=data.index)

    # convert DOB to date of attainment
    dob: pd.Series = pd.to_datetime(data[FullRegisterCols.DOB], dayfirst=True, errors='coerce')
    date_of_attainment = dob.apply(lambda x: x + pd.DateOffset(years=18))

    # map to output df
    output_df[TVVUploadCols.PREFIX] = data[FullRegisterCols.PREFIX]
    output_df[TVVUploadCols.NUMBER] = data[FullRegisterCols.NUMBER]
    output_df[TVVUploadCols.SUFFIX] = data[FullRegisterCols.SUFFIX]
    output_df[TVVUploadCols.FORENAME] = data[FullRegisterCols.FORENAME]
    output_df[TVVUploadCols.MIDDLE_NAMES] = None
    output_df[TVVUploadCols.SURNAME] = data[FullRegisterCols.SURNAME]
    output_df[TVVUploadCols.DATE_OF_ATTAINMENT] = date_of_attainment
    output_df[TVVUploadCols.ADDRESS_1] = data[FullRegisterCols.ADDRESS_1]
    output_df[TVVUploadCols.ADDRESS_2] = data[FullRegisterCols.ADDRESS_2]
    output_df[TVVUploadCols.ADDRESS_3] = data[FullRegisterCols.ADDRESS_3]
    output_df[TVVUploadCols.ADDRESS_4] = data[FullRegisterCols.ADDRESS_4]
    output_df[TVVUploadCols.ADDRESS_5] = data[FullRegisterCols.ADDRESS_5]
    output_df[TVVUploadCols.ADDRESS_6] = data[FullRegisterCols.ADDRESS_6]
    output_df[TVVUploadCols.POSTCODE] = data[FullRegisterCols.POSTCODE]
    output_df[TVVUploadCols.UPRN] = None


    return output_df