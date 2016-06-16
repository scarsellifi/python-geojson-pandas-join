# -*- coding: cp1252 -*-

import os
import pandas as pd
import json


def join(geojson, excel_dataframe, key_geojson, key_pandas, output):
    '''
    this library add 'columns' to geojson from 'pandas'
    :param geojson: geojson build with qgis
    :param exce�_dataframe: simple excel without multindex and monodimensional
    :param key_geojson:
    :param key_pandas:
    :param output
    :return:
    '''

    dataframe = pd.read_excel(excel_dataframe)


    with open(geojson) as geojson_code:
        geojson_dict = json.load(geojson_code)

    for row in geojson_dict["features"]:
        dict_temporary_data = dataframe[dataframe[key_pandas] == row[u'properties'][key_geojson]].to_dict(orient="records")
        if len(dict_temporary_data)>0:
            row[u'properties'].update(dict_temporary_data[0])

    with open(output, "w") as outfile:
            json.dump(geojson_dict, outfile)

    return geojson_dict


if __name__ == "__main__":
    link_test_geojson = os.path.join(os.getcwd(),"test", "province2006.geojson")
    link_test_excel = os.path.join(os.getcwd(),"test", "classifica.xlsx")
    link_test_output = os.path.join(os.getcwd(),"test", "output_test.geojson")
    print join(link_test_geojson, link_test_excel, u'NUTS_ID' , u'NUTS_MAP', link_test_output)


