import pandas as pd


def fn_write_pdxls(data, filename):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter', options={'strings_to_urls': False})
    for ind_sheet, df in data.items():
        df.to_excel(writer, ind_sheet, engine='xlsxwriter')
    writer.save()
    return True


def fn_read_pdxls(filename):
    xl = pd.ExcelFile(filename)
    all_sheets = xl.sheet_names
    all_sheets_data = {}
    for ind_sheet in all_sheets:
        all_sheets_data[ind_sheet] = pd.read_excel(filename, index_col=0, sheet_name=ind_sheet)
    return all_sheets_data
