from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import dash_ag_grid as dag


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

bgcolor = "#f3f3f1"  # mapbox light map land color

header = html.Div("Arapahoe Census Tract Data", className="h2 p-2 text-white bg-primary text-center")

template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}


# gdf = gpd.read_file('/Users/jamesswank/Python_projects/covid_heatmap/Census_Tracts_2020_SHAPE_WGS/Census_Tracts_2020_WGS.shp')
# gdf = gdf.to_crs("epsg:4326")
# gdf = gdf.set_geometry('geometry')
# gdf = gdf.drop(gdf.columns[[0,1,2,4,5,6,7,8,9,10,14,15]], axis=1)
# gdf['ALAND20'] = gdf['ALAND20'] / 1000000
# gdf['Pop_Density'] = gdf['P0010001'] / gdf['ALAND20'] 
# print(gdf.columns)

gdf = gpd.read_file('ArapahoeCT.shp')



df = pd.read_csv('SNAP_2021.csv')
# df['FIPS'] = df['FIPS'].astype(str)
# tgdf = gdf.merge(df, on='FIPS', how='left')

columnDefs = [
    {
        'headerName': 'Label',
        'field': 'Label'
    },
]

defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
    "minWidth": 125
}

table = dag.AgGrid(
    id='ct-grid',
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    # cellStyle=cellStyle,
    # dangerously_allow_code=True,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single"},
)

# tgdf = gdf.merge(df, on='FIPS', how='left')
# print(tgdf)

def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }



app.layout = dbc.Container(
    [
        header,
        dbc.Row(dcc.Graph(id='ct-map', figure=blank_fig(500))),
        dbc.Row(dcc.RadioItems(
                id='radio',
                options=['SNAP', 'Income', 'Households'], inline=True,
            ),
        ),
        dbc.Row(dbc.Col(table, className="py-4")),
        dcc.Store(id='processed-data', storage_type='session'),
        dcc.Store(id='household-count-data', storage_type='session'),
    ],
)

@app.callback(
    Output('household-count-data', 'data'),
    Input('radio', 'value'),
)
def get_data(radio):
    return print(radio)

@app.callback(
    Output('ct-map', 'figure'),
    Input('ct-grid', 'selectionChanged')
)
def get_figure(selected_row):
    sel_dict = selected_row[0]
    del sel_dict['Label']
    # print(sel_dict)
    df2 = pd.DataFrame.from_dict(sel_dict, orient='index', columns=['Count'])
    df2 = df2.iloc[1: , :]
    df2.index.names = ['FIPS']
    tgdf = gdf.merge(df2, on='FIPS')
    tgdf['Count'] = tgdf['Count'].str.replace(",", "")
    tgdf.fillna(0,inplace=True)
    tgdf['Count'] = (tgdf['Count'].astype(int))
    tgdf = tgdf.set_index('FIPS')
    print(tgdf)

    

    fig = px.choropleth_mapbox(tgdf, 
                                geojson=tgdf.geometry, 
                                color="Count",                               
                                locations=tgdf.index, 
                                # featureidkey="properties.TRACTCE20",
                                opacity=0.5)

    fig.update_layout(mapbox_style="carto-positron", 
                      mapbox_zoom=10.4,
                      mapbox_center={"lat": 39.65, "lon": -104.8},
                      margin={"r":0,"t":0,"l":0,"b":0},
                      uirevision='constant')


    return fig

# @app.callback(
#     Output('processed-data', 'data'),
#     Input('product', 'value')
# )
# def select_data(product):




if __name__ == "__main__":
    app.run_server(debug=True, port=8080)