import pandas as pd
from sqlalchemy import create_engine

df_target = pd.read_excel("./xxx.xlsx", engine='openpyxl')
# print(df_target)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xyz?charset=utf8")

df_region = pd.read_sql_query("SELECT * FROM `region` where region_level = 2", engine)
# print(df_region)

df_city = pd.read_sql_query("SELECT * FROM `city` where type = 2", engine)
# print(df_city)
region = None
session = engine.connect()
for i in range(df_target.shape[0]):
    if df_target.iloc[i, 0] is not None and str(df_target.iloc[i, 0]) != 'nan':
        region = df_target.iloc[i, 0]
    city = df_target.iloc[i, 1] + "市"
    store = str(df_target.iloc[i, 4]) == "是"
    if not store:
        continue
    print(region + " " + city)
    df_search_city = df_city[df_city.city_name == city]["city_code"]
    if df_search_city is not None:
        city_code = df_city[df_city.city_name == city]["city_code"].values[0]
        city_id = df_city[df_city.city_name == city]["id"].values[0]
    df_search_region = df_region[df_region.org_name == region]["org_code"]
    if df_search_region is not None:
        region_code = df_region[df_region.org_name == region]["org_code"].values[0]
        region_id = df_region[df_region.org_name == region]["id"].values[0]
    print(str(city_id) + " " + str(city_code) + " " + str(region_id) + " " + str(region_code))
    data = [
        [region_id, region_code, city_id, city_code]
    ]
    session.execute("INSERT INTO `region_city_relation`(`region_org_id`,`org_code`,`city_id`,`city_code`)"
                    "VALUES( %s, %s, %s, %s);", data)

    print()
session.close()
