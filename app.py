from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


header = html.Div("Arapahoe Census Tract Data", className="h2 p-2 text-white bg-primary text-center")

app.layout = dbc.Container(
    [
        header,
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)