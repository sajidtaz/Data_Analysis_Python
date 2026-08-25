# ============================================================
# STOCK MARKET ANALYTICS DASHBOARD
# Python + Dash + Bootstrap + Plotly
# ============================================================

import pandas as pd
import numpy as np
import plotly.express as px

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# ============================================================
# 1. LOAD DATA
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(
    BASE_DIR / "df_long.csv"
)

# Convert Date to datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%Y-%m-%d"
)

# Sort data
df = (
    df
    .sort_values(["Ticker", "Date"])
    .reset_index(drop=True)
)


# ============================================================
# 2. DASH APP
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)

app.title = "Stock Market Analytics Dashboard (Yahoo Finance)"


# ============================================================
# 3. STOCK LIST / DATE RANGE
# ============================================================

stocks = sorted(
    df["Ticker"].dropna().unique()
)

min_date = df["Date"].min()
max_date = df["Date"].max()


# ============================================================
# 4. COLOR PALETTE
# ============================================================

COLORS = {
    "navy": "#0F172A",
    "navy_light": "#1E293B",

    "blue": "#2563EB",
    "blue_light": "#DBEAFE",

    "green": "#16A34A",
    "green_light": "#DCFCE7",

    "red": "#DC2626",
    "red_light": "#FEE2E2",

    "purple": "#7C3AED",
    "purple_light": "#EDE9FE",

    "orange": "#EA580C",
    "orange_light": "#FFEDD5",

    "text": "#172033",
    "muted": "#64748B",

    "background": "#F1F5F9",
    "border": "#E2E8F0",
    "white": "#FFFFFF",

    "grid": "#E2E8F0"
}


# ============================================================
# 5. PLOTLY COLOR PALETTE
# ============================================================

STOCK_COLORS = [
    "#2563EB",
    "#16A34A",
    "#EA580C",
    "#7C3AED",
    "#DC2626",
    "#0891B2",
    "#CA8A04",
    "#DB2777",
    "#4F46E5",
    "#059669"
]


# ============================================================
# 6. COMMON STYLES
# ============================================================

PAGE_STYLE = {
    "backgroundColor": COLORS["background"],
    "minHeight": "100vh",
    "paddingBottom": "40px"
}


CARD_STYLE = {
    "border": "none",
    "borderRadius": "14px",
    "boxShadow": "0 3px 12px rgba(15, 23, 42, 0.08)",
    "backgroundColor": COLORS["white"]
}


KPI_VALUE_STYLE = {
    "fontSize": "28px",
    "fontWeight": "700",
    "color": COLORS["text"]
}


SECTION_TITLE_STYLE = {
    "fontSize": "15px",
    "fontWeight": "600",
    "color": COLORS["text"],
    "marginBottom": "10px"
}


# ============================================================
# 7. EMPTY FIGURE
# ============================================================

def create_empty_figure(message="No data available"):

    fig = px.scatter()

    fig.update_layout(
        template="plotly_white",
        title=message,
        title_x=0.02,

        margin=dict(
            l=40,
            r=30,
            t=60,
            b=40
        ),

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        ),

        paper_bgcolor=COLORS["white"],
        plot_bgcolor=COLORS["white"],

        font=dict(
            family="Arial",
            color=COLORS["text"]
        )
    )

    return fig


# ============================================================
# 8. EMPTY KPI CARD
# ============================================================

def create_empty_card(message="No data available"):

    return dbc.Card(

        dbc.CardBody(

            html.Div(
                [
                    html.Div(
                        "—",
                        style={
                            "fontSize": "28px",
                            "fontWeight": "700",
                            "color": COLORS["muted"]
                        }
                    ),

                    html.Div(
                        message,
                        className="text-muted"
                    )
                ],

                className="text-center"
            )
        ),

        style=CARD_STYLE,
        className="h-100"
    )


# ============================================================
# 9. DASHBOARD LAYOUT
# ============================================================

app.layout = dbc.Container(

    fluid=True,

    className="px-3 px-md-4 py-3",

    style=PAGE_STYLE,

    children=[


        # ====================================================
        # HEADER
        # ====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.Div(

                        [

                            html.H2(
                                "📊 Stock Market Analytics Dashboard",
                                className="fw-bold mb-1",
                                style={
                                    "color": COLORS["white"]
                                }
                            ),

                            html.P(
                                "Interactive analysis of stock performance, "
                                "growth, risk and correlation",
                                className="mb-0",
                                style={
                                    "color": "#CBD5E1"
                                }
                            )

                        ],

                        className="py-2"

                    )

                ]

            ),

            className="border-0 shadow-sm mb-4",

            style={
                "backgroundColor": COLORS["navy"],
                "borderRadius": "14px",
                "borderLeft": f"6px solid {COLORS['blue']}"
            }

        ),


        # ====================================================
        # FILTER SECTION
        # ====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.Div(

                        [

                            html.Span(
                                "⚙",
                                style={
                                    "fontSize": "18px",
                                    "marginRight": "8px",
                                    "color": COLORS["blue"]
                                }
                            ),

                            html.Span(
                                "Dashboard Filters",
                                style={
                                    "fontSize": "17px",
                                    "fontWeight": "700",
                                    "color": COLORS["text"]
                                }
                            )

                        ],

                        className="mb-3"

                    ),

                    dbc.Row(

                        [

                            # --------------------------------
                            # STOCK SELECTOR
                            # --------------------------------

                            dbc.Col(

                                [

                                    html.Label(
                                        "Select Stocks",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": COLORS["muted"]
                                        }
                                    ),

                                    dcc.Dropdown(

                                        id="stock-selector",

                                        options=[
                                            {
                                                "label": stock,
                                                "value": stock
                                            }

                                            for stock in stocks
                                        ],

                                        value=stocks,

                                        multi=True,

                                        placeholder="Select stocks...",

                                        clearable=True,

                                        style={
                                            "fontSize": "14px"
                                        }

                                    )

                                ],

                                xs=12,
                                lg=8,

                                className="mb-3 mb-lg-0"

                            ),


                            # --------------------------------
                            # DATE RANGE
                            # --------------------------------

                            dbc.Col(

                                [

                                    html.Label(
                                        "Select Date Range",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": COLORS["muted"]
                                        }
                                    ),

                                    dcc.DatePickerRange(

                                        id="date-selector",

                                        min_date_allowed=min_date.date(),

                                        max_date_allowed=max_date.date(),

                                        start_date=min_date.date(),

                                        end_date=max_date.date(),

                                        display_format="YYYY-MM-DD",

                                        start_date_placeholder_text="Start Date",

                                        end_date_placeholder_text="End Date",

                                        style={
                                            "width": "100%"
                                        }

                                    )

                                ],

                                xs=12,
                                lg=4

                            )

                        ]

                    )

                ],

                className="p-3 p-md-4"

            ),

            style=CARD_STYLE,

            className="mb-4"

        ),


        # ====================================================
        # KPI CARDS
        # ====================================================

        dbc.Row(

            [

                dbc.Col(
                    html.Div(id="kpi-stocks"),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3"
                ),

                dbc.Col(
                    html.Div(id="kpi-best"),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3"
                ),

                dbc.Col(
                    html.Div(id="kpi-growth"),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3"
                ),

                dbc.Col(
                    html.Div(id="kpi-volatility"),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3"
                )

            ],

            className="g-3 mb-3"

        ),


        # ====================================================
        # NORMALIZED PERFORMANCE
        # ====================================================

        dbc.Card(

            dbc.CardBody(

                dcc.Loading(

                    type="circle",

                    children=dcc.Graph(

                        id="performance-chart",

                        config={
                            "displaylogo": False,
                            "responsive": True
                        },

                        style={
                            "height": "520px"
                        }

                    )

                ),

                className="p-2 p-md-3"

            ),

            style={
                **CARD_STYLE,
                "borderTop": f"4px solid {COLORS['blue']}"
            },

            className="mb-4"

        ),


        # ====================================================
        # GROWTH + VOLATILITY
        # ====================================================

        dbc.Row(

            [

                # --------------------------------------------
                # TOTAL GROWTH
                # --------------------------------------------

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            dcc.Loading(

                                type="circle",

                                children=dcc.Graph(

                                    id="growth-chart",

                                    config={
                                        "displaylogo": False,
                                        "responsive": True
                                    },

                                    style={
                                        "height": "430px"
                                    }

                                )

                            ),

                            className="p-2 p-md-3"

                        ),

                        style={
                            **CARD_STYLE,
                            "borderTop": f"4px solid {COLORS['green']}"
                        },

                        className="h-100"

                    ),

                    xs=12,
                    lg=6

                ),


                # --------------------------------------------
                # ANNUAL VOLATILITY
                # --------------------------------------------

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            dcc.Loading(

                                type="circle",

                                children=dcc.Graph(

                                    id="volatility-chart",

                                    config={
                                        "displaylogo": False,
                                        "responsive": True
                                    },

                                    style={
                                        "height": "430px"
                                    }

                                )

                            ),

                            className="p-2 p-md-3"

                        ),

                        style={
                            **CARD_STYLE,
                            "borderTop": f"4px solid {COLORS['red']}"
                        },

                        className="h-100"

                    ),

                    xs=12,
                    lg=6

                )

            ],

            className="g-4 mb-4"

        ),


        # ====================================================
        # CORRELATION MATRIX
        # ====================================================

        dbc.Card(

            dbc.CardBody(

                dcc.Loading(

                    type="circle",

                    children=dcc.Graph(

                        id="correlation-chart",

                        config={
                            "displaylogo": False,
                            "responsive": True
                        },

                        style={
                            "height": "620px"
                        }

                    )

                ),

                className="p-2 p-md-3"

            ),

            style={
                **CARD_STYLE,
                "borderTop": f"4px solid {COLORS['purple']}"
            },

            className="mb-4"

        ),


        # ====================================================
        # DAILY RETURN DISTRIBUTION
        # ====================================================

        dbc.Card(

            dbc.CardBody(

                dcc.Loading(

                    type="circle",

                    children=dcc.Graph(

                        id="return-chart",

                        config={
                            "displaylogo": False,
                            "responsive": True
                        },

                        style={
                            "height": "560px"
                        }

                    )

                ),

                className="p-2 p-md-3"

            ),

            style={
                **CARD_STYLE,
                "borderTop": f"4px solid {COLORS['orange']}"
            }

        )

    ]

)


# ============================================================
# 10. CALLBACK
# ============================================================

@app.callback(

    [

        # KPI outputs

        Output(
            "kpi-stocks",
            "children"
        ),

        Output(
            "kpi-best",
            "children"
        ),

        Output(
            "kpi-growth",
            "children"
        ),

        Output(
            "kpi-volatility",
            "children"
        ),


        # Chart outputs

        Output(
            "performance-chart",
            "figure"
        ),

        Output(
            "growth-chart",
            "figure"
        ),

        Output(
            "volatility-chart",
            "figure"
        ),

        Output(
            "correlation-chart",
            "figure"
        ),

        Output(
            "return-chart",
            "figure"
        )

    ],

    [

        Input(
            "stock-selector",
            "value"
        ),

        Input(
            "date-selector",
            "start_date"
        ),

        Input(
            "date-selector",
            "end_date"
        )

    ]

)


def update_dashboard(

    selected_stocks,
    start_date,
    end_date

):


    # ========================================================
    # 1. HANDLE EMPTY STOCK SELECTION
    # ========================================================

    if not selected_stocks:

        empty_fig = create_empty_figure(
            "Please select at least one stock"
        )

        empty_card = create_empty_card(
            "No stock selected"
        )

        return (

            empty_card,
            empty_card,
            empty_card,
            empty_card,

            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig

        )


    # ========================================================
    # 2. FILTER DATA
    # ========================================================

    filtered = df[
        df["Ticker"].isin(selected_stocks)
    ].copy()


    # Convert dates

    if start_date is not None:

        start_date = pd.to_datetime(start_date)


    if end_date is not None:

        end_date = pd.to_datetime(end_date)


    # Apply date filter

    if start_date is not None:

        filtered = filtered[
            filtered["Date"] >= start_date
        ]


    if end_date is not None:

        filtered = filtered[
            filtered["Date"] <= end_date
        ]


    # ========================================================
    # 3. SORT DATA
    # ========================================================

    filtered = (

        filtered

        .sort_values(
            ["Ticker", "Date"]
        )

        .reset_index(drop=True)

    )


    # ========================================================
    # 4. HANDLE NO DATA
    # ========================================================

    if filtered.empty:

        empty_fig = create_empty_figure(
            "No data available for the selected filters"
        )

        empty_card = create_empty_card(
            "No data available"
        )

        return (

            empty_card,
            empty_card,
            empty_card,
            empty_card,

            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig

        )


    # ========================================================
    # 5. DAILY RETURN
    # ========================================================

    filtered["Daily Return"] = (

        filtered

        .groupby("Ticker")["Price"]

        .pct_change()

    )


    # ========================================================
    # 6. NORMALIZED PRICE
    # ========================================================

    filtered["Normalized Price"] = (

        filtered

        .groupby("Ticker")["Price"]

        .transform(

            lambda x:
                (x / x.iloc[0]) * 100

        )

    )


    # ========================================================
    # 7. STOCK SUMMARY
    # ========================================================

    summary = (

        filtered

        .groupby("Ticker")

        .agg(

            Start_Price=(
                "Price",
                "first"
            ),

            End_Price=(
                "Price",
                "last"
            ),

            Average_Return=(
                "Daily Return",
                "mean"
            ),

            Daily_Volatility=(
                "Daily Return",
                "std"
            )

        )

        .reset_index()

    )


    # ========================================================
    # 8. TOTAL GROWTH
    # ========================================================

    summary["Total Growth %"] = (

        (

            summary["End_Price"]

            /

            summary["Start_Price"]

        )

        - 1

    ) * 100


    # ========================================================
    # 9. ANNUALIZED VOLATILITY
    # ========================================================

    summary["Annual Volatility %"] = (

        summary["Daily_Volatility"]

        *

        np.sqrt(252)

        *

        100

    )


    # ========================================================
    # 10. KPI VALUES
    # ========================================================

    number_stocks = len(selected_stocks)


    best_stock = summary.loc[

        summary["Total Growth %"].idxmax(),

        "Ticker"

    ]


    best_growth = summary[
        "Total Growth %"
    ].max()


    most_volatile = summary.loc[

        summary["Annual Volatility %"].idxmax(),

        "Ticker"

    ]


    # ========================================================
    # 11. KPI CARDS
    # ========================================================

    kpi_label_style = {

        "fontSize": "12px",

        "fontWeight": "600",

        "color": COLORS["muted"],

        "letterSpacing": "0.5px"

    }


    # Selected Stocks

    kpi1 = dbc.Card(

        dbc.CardBody(

            [

                html.Div(
                    "SELECTED STOCKS",
                    style=kpi_label_style
                ),

                html.Div(
                    number_stocks,
                    style={
                        **KPI_VALUE_STYLE,
                        "color": COLORS["blue"]
                    }
                )

            ],

            className="text-center py-3"

        ),

        style={
            **CARD_STYLE,
            "borderTop": f"4px solid {COLORS['blue']}"
        },

        className="h-100"

    )


    # Best Performer

    kpi2 = dbc.Card(

        dbc.CardBody(

            [

                html.Div(
                    "BEST PERFORMER",
                    style=kpi_label_style
                ),

                html.Div(
                    best_stock,
                    style={
                        **KPI_VALUE_STYLE,
                        "color": COLORS["green"]
                    }
                )

            ],

            className="text-center py-3"

        ),

        style={
            **CARD_STYLE,
            "borderTop": f"4px solid {COLORS['green']}"
        },

        className="h-100"

    )


    # Highest Growth

    kpi3 = dbc.Card(

        dbc.CardBody(

            [

                html.Div(
                    "HIGHEST GROWTH",
                    style=kpi_label_style
                ),

                html.Div(

                    f"{best_growth:.1f}%",

                    style={
                        **KPI_VALUE_STYLE,
                        "color": COLORS["green"]
                    }

                )

            ],

            className="text-center py-3"

        ),

        style={
            **CARD_STYLE,
            "borderTop": f"4px solid {COLORS['green']}"
        },

        className="h-100"

    )


    # Most Volatile

    kpi4 = dbc.Card(

        dbc.CardBody(

            [

                html.Div(
                    "MOST VOLATILE",
                    style=kpi_label_style
                ),

                html.Div(
                    most_volatile,
                    style={
                        **KPI_VALUE_STYLE,
                        "color": COLORS["red"]
                    }
                )

            ],

            className="text-center py-3"

        ),

        style={
            **CARD_STYLE,
            "borderTop": f"4px solid {COLORS['red']}"
        },

        className="h-100"

    )


    # ========================================================
    # 12. NORMALIZED PERFORMANCE
    # ========================================================

    performance_fig = px.line(

        filtered,

        x="Date",

        y="Normalized Price",

        color="Ticker",

        color_discrete_sequence=STOCK_COLORS,

        title="Normalized Stock Performance",

        labels={

            "Normalized Price":
                "Performance (Base = 100)",

            "Date":
                "Date",

            "Ticker":
                "Stock"

        }

    )


    performance_fig.update_layout(

        template="plotly_white",

        hovermode="x unified",

        margin=dict(
            l=55,
            r=30,
            t=65,
            b=50
        ),

        title_x=0.02,

        legend_title_text="Stock",

        font=dict(
            family="Arial",
            size=12,
            color=COLORS["text"]
        ),

        paper_bgcolor=COLORS["white"],

        plot_bgcolor=COLORS["white"]

    )


    performance_fig.update_xaxes(

        showgrid=True,

        gridcolor=COLORS["grid"]

    )


    performance_fig.update_yaxes(

        showgrid=True,

        gridcolor=COLORS["grid"]

    )


    # ========================================================
    # 13. TOTAL GROWTH
    # ========================================================

    growth_data = (

        summary

        .sort_values(
            "Total Growth %",
            ascending=False
        )

    )


    growth_fig = px.bar(

        growth_data,

        x="Ticker",

        y="Total Growth %",

        text="Total Growth %",

        color="Total Growth %",

        color_continuous_scale=[
            "#BBF7D0",
            "#16A34A"
        ],

        title="Total Stock Growth",

        labels={

            "Total Growth %":
                "Total Growth (%)",

            "Ticker":
                "Stock"

        }

    )


    growth_fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside"

    )


    growth_fig.update_layout(

        template="plotly_white",

        margin=dict(
            l=50,
            r=30,
            t=65,
            b=50
        ),

        title_x=0.02,

        font=dict(
            family="Arial",
            size=12,
            color=COLORS["text"]
        ),

        paper_bgcolor=COLORS["white"],

        plot_bgcolor=COLORS["white"],

        coloraxis_showscale=False

    )


    growth_fig.update_xaxes(
        showgrid=False
    )


    growth_fig.update_yaxes(

        showgrid=True,

        gridcolor=COLORS["grid"]

    )


    # ========================================================
    # 14. ANNUAL VOLATILITY
    # ========================================================

    volatility_data = (

        summary

        .sort_values(
            "Annual Volatility %",
            ascending=False
        )

    )


    volatility_fig = px.bar(

        volatility_data,

        x="Ticker",

        y="Annual Volatility %",

        text="Annual Volatility %",

        color="Annual Volatility %",

        color_continuous_scale=[
            "#FECACA",
            "#DC2626"
        ],

        title="Annualized Volatility",

        labels={

            "Annual Volatility %":
                "Annual Volatility (%)",

            "Ticker":
                "Stock"

        }

    )


    volatility_fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside"

    )


    volatility_fig.update_layout(

        template="plotly_white",

        margin=dict(
            l=50,
            r=30,
            t=65,
            b=50
        ),

        title_x=0.02,

        font=dict(
            family="Arial",
            size=12,
            color=COLORS["text"]
        ),

        paper_bgcolor=COLORS["white"],

        plot_bgcolor=COLORS["white"],

        coloraxis_showscale=False

    )


    volatility_fig.update_xaxes(
        showgrid=False
    )


    volatility_fig.update_yaxes(

        showgrid=True,

        gridcolor=COLORS["grid"]

    )


    # ========================================================
    # 15. CORRELATION MATRIX
    # ========================================================

    correlation_data = (

        filtered

        .pivot(

            index="Date",

            columns="Ticker",

            values="Daily Return"

        )

    )


    correlation_matrix = (

        correlation_data

        .corr()

    )


    correlation_fig = px.imshow(

        correlation_matrix,

        text_auto=".2f",

        title="Daily Return Correlation",

        color_continuous_scale=[
            "#DC2626",
            "#F8FAFC",
            "#2563EB"
        ],

        zmin=-1,

        zmax=1,

        aspect="auto",

        labels={
            "color": "Correlation"
        }

    )


    correlation_fig.update_layout(

        template="plotly_white",

        margin=dict(
            l=60,
            r=60,
            t=65,
            b=60
        ),

        title_x=0.02,

        font=dict(
            family="Arial",
            size=12,
            color=COLORS["text"]
        ),

        paper_bgcolor=COLORS["white"],

        plot_bgcolor=COLORS["white"]

    )


    # ========================================================
    # 16. DAILY RETURN DISTRIBUTION
    # ========================================================

    return_data = (

        filtered

        .dropna(
            subset=["Daily Return"]
        )

    )


    if return_data.empty:

        return_fig = create_empty_figure(
            "No daily return data available"
        )

    else:

        return_fig = px.histogram(

            return_data,

            x="Daily Return",

            color="Ticker",

            color_discrete_sequence=STOCK_COLORS,

            nbins=60,

            marginal="box",

            title="Daily Return Distribution",

            opacity=0.60,

            barmode="overlay",

            labels={

                "Daily Return":
                    "Daily Return",

                "count":
                    "Frequency"

            }

        )


        return_fig.update_layout(

            template="plotly_white",

            margin=dict(
                l=50,
                r=30,
                t=65,
                b=50
            ),

            title_x=0.02,

            font=dict(
                family="Arial",
                size=12,
                color=COLORS["text"]
            ),

            paper_bgcolor=COLORS["white"],

            plot_bgcolor=COLORS["white"],

            legend_title_text="Stock"

        )


        return_fig.update_xaxes(

            showgrid=True,

            gridcolor=COLORS["grid"]

        )


        return_fig.update_yaxes(

            showgrid=True,

            gridcolor=COLORS["grid"]

        )


    # ========================================================
    # 17. RETURN EVERYTHING
    # ========================================================

    return (

        kpi1,
        kpi2,
        kpi3,
        kpi4,

        performance_fig,

        growth_fig,

        volatility_fig,

        correlation_fig,

        return_fig

    )


# ============================================================
# 18. RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True
    )