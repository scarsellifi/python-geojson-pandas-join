# -*- coding: cp1252 -*-

import os
import pandas as pd
import json



def join(geojson, excel_dataframe, key_geojson, key_pandas, output, missing_columns=0, missing_rows=0, type_dataframe = False):
    """ this library add 'columns' to geojson from 'excel' well structured file
    :param geojson: geojson build with qgis (url)
    :param excel_dataframe: simple excel without multindex and monodimensional (url)
    :param key_geojson: key column
    :param key_pandas: key column
    :param output: url
    :param missing_columns: number of cell with NAN value for row to drop
    :param missing_rows: number of cell with NAN value for row to drop
    :return: none
    """
    if type_dataframe == False:
        dataframe = pd.read_excel(excel_dataframe)
    else:
        dataframe = excel_dataframe

    # geojson doesn't like nan!
    dataframe.dropna(inplace=True, axis=1, thresh=missing_columns)
    dataframe.dropna(inplace=True, axis=0, thresh=missing_rows)
    dataframe.fillna(0, inplace = True)

    with open(geojson) as geojson_code:
        geojson_dict = json.load(geojson_code)

    for row in geojson_dict["features"]:
        dict_temporary_data = dataframe[dataframe[key_pandas] == row[u'properties'][key_geojson]] \
            .to_dict(orient="records")
        if len(dict_temporary_data) > 0:
            row[u'properties'].update(dict_temporary_data[0])

    with open(output, "w") as outfile:
        json.dump(geojson_dict, outfile)

    if type_dataframe == False:
        return "executed " + geojson + " " + excel_dataframe
    else:
        return "executed " + geojson + " " + "dataframe"

if __name__ == "__main__":
    # link_test_geojson = r"E:\Dropbox\Dropbox\0_DB\0_SDMX\nuts2.json"
    # link_test_excel = r"E:\Dropbox\Dropbox\0_DB\0_SDMX\lfst_r_lfe2emprt.xlsx"
    #print join(link_test_geojson, link_test_excel, u'NUTS_ID', u'CodiceMAP', link_test_output, missing_columns=2)

    link_test_geojson = os.path.join(os.getcwd(), "test", "province2010_2006.geojson")
    link_test_excel = os.path.join(os.getcwd(), "test", "classifica.xlsx")
    link_test_output = os.path.join(os.getcwd(), "test", "output_test.geojson")
    print join(link_test_geojson, link_test_excel, u'nuts_id', u'NUTS_MAP', link_test_output, missing_columns=2)