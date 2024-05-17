import pandas as pd

file = "excel.xlsx"
xl = pd.ExcelFile(file)
df1 = xl.parse(xl.sheet_names[0])
keys = df1.keys()


def get_excel_data(dataframe):
    data = [['Ведомость на семинар', '', '', '', '', '', '', '', '', '', '', '']]
    for row in range(len(dataframe)):
        row_data = []
        for columns in range(len(keys)):
            row_data.append(dataframe[keys[columns]][row])
        data.append(row_data)
    print(data)


get_excel_data(df1)
