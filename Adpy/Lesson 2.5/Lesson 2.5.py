import pandas as pd
import os


PATH = os.path.abspath("files")


def find_top3(query_years):
    temp = []
    for year in query_years:
        filename = PATH + "\yob" + str(year) + ".txt"
        df_temp = pd.read_csv(os.path.abspath(filename), sep=',', encoding='utf-8', header=None,
                              names=["Name", "Gender", "Count"])
        temp.append(df_temp)
    res_df = pd.concat(temp).reset_index(drop=True)
    res_sort_df = res_df.groupby(['Name']).sum().sort_values('Count', ascending=False)
    return res_sort_df.head(3)


def count_dinamics(query_years):
    temp = []
    for year in query_years:
        filename = PATH + "\yob" + str(year) + ".txt"
        print(filename)
        df_temp = pd.read_csv(os.path.abspath(filename), sep=',', encoding='utf-8', header=None,
                              names=["Gender", "Count"])
        df_temp["Year"] = year
        temp.append(df_temp)
    res_df = pd.concat(temp).reset_index(drop=True)
    res_sort_df = res_df.groupby(['Gender', 'Year']).sum().sort_values('Count', ascending=False)
    return res_sort_df.unstack()


if __name__ == "__main__":
    #print(find_top3([1880]))
    #print(find_top3([1900, 1950, 2000]))
    print(count_dinamics([1900, 1950, 2000]))
