from collections import abc
import numbers

import pyintergraph


def get_c_type(v):
    if isinstance(v, str):
        return "string"
    elif isinstance(v, dict):
        return "object"
    elif isinstance(v, bool):
        return "uint8_t"
    elif isinstance(v, int):
        if -32768 <= v <= 32767:
            return "int16_t"
        elif -2147483648 <= v <= 2147483647:
            return "int32_t"
        elif -(2**63) <= v <= (2**63) - 1:
            return "int64_t"
        else:
            raise pyintergraph.PyIntergraphInferException(
                "Value {v} does not fit in c++ datatypes of graph_tools !"
            )
    elif isinstance(v, float):
        if pyintergraph.USE_LONG_DOUBLE:
            return "long double"
        else:
            return "double"
    elif issubclass(type(v), numbers.Number):
        if pyintergraph.USE_LONG_DOUBLE:
            return "long double"
        else:
            return "double"
    else:
        raise pyintergraph.PyIntergraphInferException(
            "Non supported Type in Attributes!"
        )


def get_best_fitting_type(c_types):
    if "object" in c_types:
        return "python::object"
    elif "string" in c_types:
        return "string"

    if "long double" in c_types:
        return "long double"
    elif "double" in c_types:
        return "double"
    elif "int64_t" in c_types:
        return "int64_t"
    elif "int32_t" in c_types:
        return "int32_t"
    elif "int16_t" in c_types:
        return "int16_t"
    elif "uint8_t" in c_types:
        return "uint8_t"


def infer_type(values, as_vector=True):
    # check for types in Iterable
    if (
        isinstance(values, abc.Iterable)
        and not isinstance(values, str)
        and not isinstance(values, dict)
    ):
        c_types = {get_c_type(v) for v in values}
    else:
        c_types = get_c_type(values)

    number_types = ["long double", "double", "long", "int", "short", "bool"]
    if any(t in number_types for t in c_types) and not all(
        t in number_types for t in c_types
    ):
        raise pyintergraph.PyIntergraphInferException(
            "Cannot mix datatypes ! Found {}".format(c_types)
        )

    best_fit = get_best_fitting_type(c_types)
    if as_vector:
        return f"vector<{best_fit}>"
    return best_fit
