import numpy as np

from functools import wraps
from unittest.mock import patch
from typing import Any


def mock_flojoy_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


patch("flojoy.flojoy", mock_flojoy_decorator).start()

import MATRIX


def test_MATRIX():
    # create the two matrices
    m1: Any = MATRIX.MATRIX([], {"row": 3, "column": 4})

    # Check if they are equal
    assert m1.m.shape == (3, 4)