from flojoy import flojoy, Plotly, OrderedPair, DataFrame, Matrix, Vector
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from nodes.VISUALIZERS.template import plot_layout


@flojoy
def LINE(default: OrderedPair | DataFrame | Matrix | Vector) -> Plotly:
    """The LINE node creates a Plotly Line visualization for a given input data container.

    Inputs
    ------
    default : OrderedPair|DataFrame|Matrix|Vector
        the DataContainer to be visualized

    Returns
    -------
    Plotly
        the DataContainer containing Plotly Line visualization of the input data
    """

    layout = plot_layout(title="LINE")
    fig = go.Figure(layout=layout)

    match default:
        case OrderedPair():
            x = default.x
            if isinstance(default.x, dict):
                dict_keys = list(default.x.keys())
                x = default.x[dict_keys[0]]
            y = default.y
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
        case DataFrame():
            df = default.m
            first_col = df.iloc[:, 0]
            is_timeseries = False
            if pd.api.types.is_datetime64_any_dtype(first_col):
                is_timeseries = True
            if is_timeseries:
                for col in df.columns:
                    if col != df.columns[0]:
                        fig.add_trace(
                            go.Scatter(
                                y=df[col].values,
                                x=first_col,
                                mode="lines",
                                name=col,
                            )
                        )
            else:
                for col in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            y=df[col].values,
                            x=df.index,
                            mode="lines",
                            name=col,
                        )
                    )

        case Matrix():
            m = default.m

            num_rows, num_cols = m.shape

            x_ticks = np.arange(num_cols)

            for i in range(num_rows):
                fig.add_trace(
                    go.Scatter(x=x_ticks, y=m[i, :], name=f"Row {i+1}", mode="lines")
                )

            fig.update_layout(xaxis_title="Column", yaxis_title="Value")
        case Vector():
            y = default.v
            x = np.arange(len(y))
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))

    return Plotly(fig=fig)
