import pandas as pd
import os


PATH = os.path.abspath("files")


def find_top3(query_years):
    temp = []
    for year in query_years:
        filename = PATH + "\yob" + str(year) + ".txt"
        df_temp = pd.read_csv(os.path.abspath(filename), sep=',', encoding='utf-8', header=None,
                              names=["Name", "Gender", "Count"])
        df_temp['Year'] = year
        temp.append(df_temp)
    res_df = pd.concat(temp).reset_index(drop=True)
    res_sort_df = res_df.groupby(['Name']).head().sort_values('Count', ascending=False)
    return res_sort_df.head(3)


if __name__ == "__main__":
    print(find_top3([1880]))
    print(find_top3([1900, 1950, 2000]))
    #
    # df_1 = pd.read_csv(os.path.abspath('files\yob1900.txt'), sep=',', encoding='utf-8', header=None,
    #                           names=["Name", "Gender", "Count"])
    # df_1['Year'] = '1900'
    # df_2 = pd.read_csv(os.path.abspath('files\yob1950.txt'), sep=',', encoding='utf-8', header=None,
    #                    names=["Name", "Gender", "Count"])
    # df_2['Year'] = '1950'
    # df_3 = pd.read_csv(os.path.abspath('files\yob2000.txt'), sep=',', encoding='utf-8', header=None,
    #                    names=["Name", "Gender", "Count"])
    # df_3['Year'] = '2000'
    # res = pd.concat([df_1, df_2, df_3])
    # group = res.groupby(["Name"]).head().sort_values('Count', ascending=False)
    # print(group.head(3))
    #
    # #res_df = pd.concat(temp).reset_index(drop=True)