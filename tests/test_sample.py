import pytest
from sample import add


@pytest.mark.sample
@pytest.mark.parametrize("x, y, expected", [
    (2, 3, 5),
    (-2, 3, 1),
    (2, -3, -1),
    (0, 0, 0),
    (1, 1, 2),
])
def test_add(x, y, expected):
    assert add(x, y) == expected
