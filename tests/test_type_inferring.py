import pytest

import pyintergraph
from pyintergraph.infer import infer_type


try:
    import numpy as np

    def test_numpy_type():
        assert infer_type(np.float(1.5), as_vector=False) == "double"


    def test_numpy_type_long():
        pyintergraph.USE_LONG_DOUBLE = True
        assert infer_type(np.float(1.5), as_vector=False) == "long double"
        pyintergraph.USE_LONG_DOUBLE = False
except ImportError:
    pass


def type_check_vector():
    yield list(range(0,50)), "vector<int16_t>"
    yield ["mein", "dein", "unser", "wir"], "vector<string>"
    yield [True, False, True, False], "vector<uint8_t>"


def type_check_single():
    yield 1, "int16_t"
    yield 1.5, "double"
    yield "test", "string"
    yield True, "uint8_t"
    yield {"tets": 1, "asd": 3}, "python::object"
    yield 2147483649, "int64_t"

@pytest.mark.infer_type
@pytest.mark.parametrize("testvals", type_check_vector())
def test_infer_type_vectors(testvals):
    _in, _out = testvals
    assert infer_type(_in, as_vector=True) == _out


@pytest.mark.infer_type
@pytest.mark.parametrize("testvals", type_check_single())
def test_infer_type_single(testvals):
    _in, _out = testvals
    assert infer_type(_in, as_vector=False) == _out


def test_long_double():
    pyintergraph.USE_LONG_DOUBLE = True
    assert infer_type(2.5, as_vector=False) == "long double"
    pyintergraph.USE_LONG_DOUBLE = False


def test_raise_infer_exception():
    invalids = [
        ["mein", "dein", 56, 4.3, "haben"],
        [2**63]
    ]
    for invalid in invalids:
        with pytest.raises(pyintergraph.PyIntergraphInferException):
            infer_type(invalid)