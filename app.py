import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Source+Sans+Pro&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Slide Digital"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(html.Img(src=app.get_asset_url('favicon.ico')), className="header-emoji"),
                html.Div(
                    children=[
                        html.H1(children="Slide Digital", className="header-title"),
                        html.P( children="Artists' Data Virtualization & Analytics", className="header-description",),
                        ],
                        className="header-g-title"
                        )    
            ],
           
           className="header", 
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Artist", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Platform", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
                # Notofication Area
                html.Div(
                    children=[
                        html.Div(children="Notification", className="menu-title"),
                        html.Div(html.Img(src=app.get_asset_url('not.png'),style={'height':'80%', 'width':'80%'} ),),
                    ],
                className="notification"
                ),
                

            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Sportify", className="platform-title"),
                        html.P(children="Followers -----      5.6M"),
                        html.P(children="Listeners -----      700K"),
                        html.P(children="Popularity -----     90"),
                        html.P(children="Playlist Reach ----- 5.6M"),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="BoomPlay", className="platform-title"),
                        html.P(children="Followers -----      5.6M"),
                        html.P(children="Listeners -----      700K"),
                        html.P(children="Popularity -----     90"),
                        html.P(children="Playlist Reach ----- 5.6M"),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Youtube", className="platform-title"),
                        html.P(children="Channel Subscribers ---2.1M"),
                        html.P(children="Channel Views -----    700K"),
                        html.P(children="Daily Video Viewers -- 500K"),
                        
                    ]
                ),
                  html.Div(
                    children=[
                        html.Div(children="TickTok", className="platform-title"),
                        html.P(children="Followers ---2.1M"),
                        html.P(children="Likes ----- 700K"),
                        html.P(children="Views ----- 500K"),
                        
                    ]
                )
            ],
            className="platform-card",
        ),
        
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.H1(children="World Wide Trends", className="map-title"),
        html.Div(
            children = [
                html.Img(src=app.get_asset_url('map.png'))
            ],
            className="map"
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Revenue Made",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},  # dollar sign is here
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Total Streams/ Day", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
