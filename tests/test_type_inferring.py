import pytest

from pyintergraph.infer import infer_type

def type_check():
    yield list(range(0,50)), "int"
    yield ["mein", "dein", "unser", "wir"], "string"
    yield ["mein", "dein", 56, 4.3, "haben"], "string"
    yield [1, 2, 3, 4, 5, 3.5, 4.5], "float"
    yield  [True, False, True, False], "bool"
    yield 1, "int"
    yield 1.5, "float"
    yield "test", "string"
    yield True, "bool"
    yield {"tets": 1, "asd": 3}, "object"
@pytest.mark.infer_type
@pytest.mark.parametrize("testvals", type_check())
def test_infer_type(testvals):
    _in, _out = testvals
    assert infer_type(_in) == _out
