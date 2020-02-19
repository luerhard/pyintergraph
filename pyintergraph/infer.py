from collections import abc
import numbers

import pyintergraph

def infer_type(value):

    def get_vector_type(c_type):
        if c_type == "int":
            return "vector<int>"
        elif c_type == "float":
            return "vector<float>"
        elif c_type == "string":
            return "vector<string>"
        elif c_type == "bool":
            return "vector<uint8_t>"
        else:
            return "object"

    def get_c_type(v):
        if isinstance(v, str) or v == str:
            return "string"
        elif isinstance(v, bool) or v == bool:
            return "bool"
        elif isinstance(v, int) or v == int:
            return "int"
        elif isinstance(v, float) or v == float:
            return "float"
        elif issubclass(v, numbers.Number):
            return "float"
        else:
            raise Exception("Non supported Type in Attributes!")

    if isinstance(value, abc.Iterable):
        if isinstance(value, str):
            return "string"
        if type(value) == dict:
            return "object"

        # check for types in Iterable
        types = set(type(v) for v in value)
        if len(types) == 1:
            c_type = get_c_type(types.pop())
            vector_type = get_vector_type(c_type)
            return vector_type
        else:
            raise pyintergraph.PyIntergraphInferException(
                    f"Multiple Types Found: {types}. graph_tool cannot handle that")

    return get_c_type(value)
