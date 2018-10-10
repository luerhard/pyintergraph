import collections

def infer_type(value):

    def get_c_type(v):
        if isinstance(v, str) or v == str:
            return "string"
        elif isinstance(v, int) or v == int:
            return "int"
        elif isinstance(v, float) or v == float:
            return "float"
        elif isinstance(v, bool) or v == bool:
            return "bool"
        else:
            return "object"
    if isinstance(value, collections.Iterable):
        if len(value) == 1:
            return get_c_type(value)
        elif len(value) > 1:
            types = set(type(v) for v in value)
            if len(types) == 1:
                return get_c_type(types.pop())
            else:
                return "string"
    else:
        return get_c_type(value)
    