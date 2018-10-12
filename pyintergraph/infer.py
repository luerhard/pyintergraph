import collections

def infer_type(value):

    def is_primitive(val):
        primitives = (int, bool, float, str)
        return val in primitives

    def get_c_type(v):
        if isinstance(v, str) or v == str:
            return "string"
        elif isinstance(v, bool) or v == bool:
            return "bool"
        elif isinstance(v, int) or v == int:
            return "int"
        elif isinstance(v, float) or v == float:
            return "float"
        else:
            raise Exception("Non supported Type in Attributes!")

    if isinstance(value, collections.Iterable):
        if type(value) != dict:
            if len(value) == 1:
                return get_c_type(value)
            elif len(value) > 1:
                types = set(type(v) for v in value)
                if len(types) == 1:
                    return get_c_type(types.pop())
                elif len(types) == 2 and types == set([float, int]):
                    return "float"
                else:
                    return "string"
        else:
            return "object"
    else:
        return get_c_type(value)
