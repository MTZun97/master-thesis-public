import dash


def crp_create_table():
    headers = ["Parameter", "Alkaline", "PEM"]
    rows_data = [
        ("Single Curve Fitting Decline Rate", "4.4%", "3.4%"),
        ("Double Curve Fitting Decline Rate", "3%", "4.3%"),
        ("Scaling Factor", "0.37", "0.6"),
        ("Learning Rate", "8%", "10%"),
    ]

    table_rows = [
        dash.html.Tr(
            [dash.html.Th(header, style={"padding": "0 1vh"}) for header in headers]
        )
    ] + [
        dash.html.Tr([dash.html.Td(cell, style={"padding": "0 1vh"}) for cell in row])
        for row in rows_data
    ]

    return dash.html.Table(table_rows, className="div-table")


def create_timeline_table():
    headers = ["Scenario", "LCOE", "Electrolzyer"]
    rows_data = [
        ("Optimistic", "Average percentage decline", "R&D + scaling + learning rate"),
        ("Pessimistic", "Constant", "R&D"),
    ]

    table_rows = [
        dash.html.Tr(
            [dash.html.Th(header, style={"padding": "0 1vh"}) for header in headers]
        )
    ] + [
        dash.html.Tr([dash.html.Td(cell, style={"padding": "0 1vh"}) for cell in row])
        for row in rows_data
    ]

    return dash.html.Table(table_rows, className="div-table")
