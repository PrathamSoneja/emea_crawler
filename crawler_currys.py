import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os


def cleanDF(df):
    df.index+=2
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'row_no'}, inplace=True)
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True, axis=1)

    obj_cols = df.columns[df.dtypes == "object"]
    for col in obj_cols:
        df[col] = df[col].str.lower()
    return df


def findMisMatchCol(df_1, df_2):
    col_1 = df_1.columns
    col_2 = df_2.columns
    temp_1 = [ele for ele in col_1 if ele not in col_2]
    temp_2 = [ele for ele in col_2 if ele not in col_1]
    return df_1, df_2, temp_1, temp_2

def findIssues(df_1, df_2):
    col_name = df_1.columns.tolist()
    col_name.remove("row_no")
    col_name.remove("Date")
    col_name.remove("id")
    device_list_1 = np.unique(df_1['Device']).tolist()
    device_list_2 = np.unique(df_2['Device']).tolist()

    dv_1 = [dv for dv in device_list_1 if dv not in device_list_2]
    dv_2 = [dv for dv in device_list_2 if dv not in device_list_1]
    missing_dv_1 = {}
    for i in range(len(dv_1)):
        dv_index_not_in_file_2 = df_1.where(df_1['Device'] == dv_1[i]).dropna(axis=0, how='all')['row_no'].tolist()
        missing_dv_1[dv_1[i]] = dv_index_not_in_file_2

    missing_dv_2 = {}
    for i in range(len(dv_2)):
        dv_index_not_in_file_1 = df_2.where(df_2['Device'] == dv_2[i]).dropna(axis=0, how='all')['row_no'].tolist()
        missing_dv_2[dv_2[i]] = dv_index_not_in_file_1

    for ele in dv_1:
        if ele in device_list_1:
            device_list_1.remove(ele)
    for ele in dv_2:
        if ele in device_list_2:
            device_list_2.remove(ele)

    df_1.fillna('Empty', inplace=True)
    df_2.fillna('Empty', inplace=True)

    disc = {}
    idx_1_not_in_2 = []
    idx_2_not_in_1 = []
    idx_main = []

    for i in range(len(device_list_1)):
        device = device_list_1[i]
        temp_11 = df_1.where(df_1['Device'] == device).dropna(axis=0, how='all')
        temp_21 = df_2.where(df_2['Device'] == device).dropna(axis=0, how='all')
        var_list = np.unique(temp_11['Variant']).tolist()

        for j in range(len(var_list)):
            var = var_list[j]
            temp_12 = temp_11.where(temp_11['Variant'] == var).dropna(axis=0, how='all')
            temp_22 = temp_21.where(temp_21['Variant'] == var).dropna(axis=0, how='all')
            device_colour_list = np.unique(temp_12['Device Colour']).tolist()

            for m in range(len(device_colour_list)):
                dvc = device_colour_list[m]
                temp_14 = temp_12.where(temp_12['Device Colour'] == dvc).dropna(axis=0, how='all')
                temp_24 = temp_22.where(temp_22['Device Colour'] == dvc).dropna(axis=0, how='all')
                hk = []
                idx_main = f"{device}_{var}_{dvc}"

                if temp_14.shape == temp_24.shape:
                    temp_14.reset_index(inplace=True, drop=True)
                    temp_24.reset_index(inplace=True, drop=True)
                    bool_df = pd.DataFrame(temp_14[col_name] == temp_24[col_name])
                    t = np.where(bool_df.values == False)
                    k = np.stack((t[0], t[1]), axis=1)
                    for f in range(len(k)):
                        hk += [[col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'], temp_24.iloc[k[f][0]]['row_no']]]
                        print(device, col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'],
                              temp_24.iloc[k[f][0]]['row_no'])
                    if len(hk) != 0:
                        disc[idx_main] = hk

                if temp_14.shape != temp_24.shape:
                    temp_14.reset_index(inplace=True, drop=True)
                    temp_24.reset_index(inplace=True, drop=True)

                    if len(temp_14) > len(temp_24):
                        idx_ = temp_14.iloc[len(temp_14) - len(temp_24):].index.values.tolist()
                        idx_1_not_in_2 += temp_14.iloc[idx_]['row_no'].values.tolist()
                        temp_14.drop(idx_, axis=0, inplace=True)

                        if len(temp_14) == len(temp_24):
                            temp_14.reset_index(inplace=True, drop=True)
                            temp_24.reset_index(inplace=True, drop=True)
                            bool_df = pd.DataFrame(temp_14[col_name] == temp_24[col_name])
                            t = np.where(bool_df.values == False)
                            k = np.stack((t[0], t[1]), axis=1)
                            for f in range(len(k)):
                                hk += [[col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'],
                                        temp_24.iloc[k[f][0]]['row_no']]]
                                print(device, col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'],
                                      temp_24.iloc[k[f][0]]['row_no'])
                            if len(hk) != 0:
                                disc[idx_main] = hk

                    if len(temp_14) < len(temp_24):
                        idx_ = temp_24.iloc[len(temp_24) - len(temp_14):].index.values.tolist()
                        idx_2_not_in_1 += temp_24.iloc[idx_]['row_no'].values.tolist()
                        temp_24.drop(idx_, axis=0, inplace=True)

                        if len(temp_14) == len(temp_24):
                            temp_14.reset_index(inplace=True, drop=True)
                            temp_24.reset_index(inplace=True, drop=True)
                            bool_df = pd.DataFrame(temp_14[col_name] == temp_24[col_name])
                            t = np.where(bool_df.values == False)
                            k = np.stack((t[0], t[1]), axis=1)
                            for f in range(len(k)):
                                hk += [[col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'],
                                        temp_24.iloc[k[f][0]]['row_no']]]
                                print(device, col_name[k[f][1]], temp_14.iloc[k[f][0]]['row_no'],
                                      temp_24.iloc[k[f][0]]['row_no'])
                            if len(hk) != 0:
                                disc[idx_main] = hk

    return missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1

def process_curry(df_1, df_2):
    df_1 = cleanDF(df_1)
    df_2 = cleanDF(df_2)
    df_1, df_2, temp_1, temp_2 = findMisMatchCol(df_1, df_2)
    missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1 = findIssues(df_1, df_2)
    return temp_1, temp_2, missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1

if __name__ == '__main__':
    df_1 = pd.read_excel("C:\\Crawler_flask_app\\temp_xlsx\\cpw_uk_data 4th feb revised.xlsx")
    df_2 = pd.read_excel("C:\\Crawler_flask_app\\temp_xlsx\\cpw_uk_data 5th feb revised.xlsx")
    col_1, col_2, missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1 = process_xlsx(df_1, df_2)

    output = {'columns in file 1 but not in file 2': col_1, 'columns in file 2 but not in file 1': col_2,
              'devices not in file 2': [missing_dv_1], 'devices not in file 1': [missing_dv_2],
              'indices not in file 1': [idx_2_not_in_1], 'indices not in file 2': [idx_1_not_in_2],
              'mis matched values': [disc]}
    print(output)

