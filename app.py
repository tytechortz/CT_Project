from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

bgcolor = "#f3f3f1"  # mapbox light map land color

header = html.Div("Arapahoe Census Tract Data", className="h2 p-2 text-white bg-primary text-center")

template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}


gdf = gpd.read_file('/Users/jamesswank/Python_projects/covid_heatmap/Census_Tracts_2020_SHAPE_WGS/Census_Tracts_2020_WGS.shp')
gdf = gdf.to_crs("epsg:4326")
gdf = gdf.set_geometry('geometry')

gdf = gdf.drop(gdf.columns[[1,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis=1)

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
        dcc.Store(id='processed-data', storage_type='session'),
    ],
)

@app.callback(
    Output('ct-map', 'figure'),
    Input('processed-data', 'data')
)
def get_figure(processed_data):
    

    fig = px.choropleth_mapbox(gdf, 
                                geojson=gdf.geometry, 
                                color="TRACTCE20",                               
                                locations=gdf.index, 
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