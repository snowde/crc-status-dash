if not vertical:
    app.layout = html.Div([
        dcc.Tabs(
            tabs=[
                {'label': 'Market Value', 'value': 1},
                {'label': 'Usage Over Time', 'value': 2},
                {'label': 'Predictions', 'value': 3},
                {'label': 'Target Pricing', 'value': 4},
            ],
            value=3,
            id='tabs',
            vertical=vertical
        ),
        html.Div(id='tab-output')
    ], style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    })

else:
    app.layout = html.Div([
        html.Div(
            dcc.Tabs(
                tabs=[
                    {'label': 'Market Value', 'value': 1},
                    {'label': 'Usage Over Time', 'value': 2},
                    {'label': 'Predictions', 'value': 3},
                    {'label': 'Target Pricing', 'value': 4},
                ],
                value=3,
                id='tabs',
                vertical=vertical,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left'
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })