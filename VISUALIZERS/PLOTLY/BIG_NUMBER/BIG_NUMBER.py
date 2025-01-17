from flojoy import (
    flojoy,
    Plotly,
    OrderedPair,
    DefaultParams,
    SmallMemory,
    Scalar,
    Vector,
)
import plotly.graph_objects as go
from nodes.VISUALIZERS.template import plot_layout

MEMORY_KEY = "BIG_NUMBER_MEMORY_KEY"


@flojoy(inject_node_metadata=True)
def BIG_NUMBER(
    default: OrderedPair | Scalar | Vector,
    default_params: DefaultParams,
    suffix: str,
    prefix: str,
    title: str,
    relative_delta: bool = True,
) -> Plotly:
    """The BIG_NUMBER node generates a Plotly figure, displaying a big number with an optional prefix and suffix.

    Inputs
    ------
    default : OrderedPair|Scalar|Vector
        the DataContainer to be visualized

    Parameters
    ----------
    relative_delta : bool
        whether to show relative delta from last run along with big number
    suffix : str
        any suffix to show with big number
    prefix : str
        any prefix to show with big number
    title : str
        title of the plot, default "BIG_NUMBER"

    Returns
    -------
    Plotly
        the DataContainer containing Plotly big number visualization
    """

    job_id = default_params.job_id
    node_name = __name__.split(".")[-1]
    layout = plot_layout(title=title if title else node_name)
    fig = go.Figure(layout=layout)

    prev_num = SmallMemory().read_memory(job_id, MEMORY_KEY)
    match default:
        case OrderedPair():
            big_num = default.y[-1]
        case Scalar():
            big_num = default.c
        case Vector():
            big_num = default.v[-1]
    val_format = ".1%" if relative_delta is True else ".1f"
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=int(float(big_num)),
            domain={"y": [0, 1], "x": [0, 1]},
            number={"prefix": prefix, "suffix": suffix},
            delta=None
            if prev_num is None
            else {
                "reference": int(float(prev_num)),
                "relative": relative_delta,
                "valueformat": val_format,
            },
        )
    )
    SmallMemory().write_to_memory(job_id, MEMORY_KEY, str(float(big_num)))

    return Plotly(fig=fig)
