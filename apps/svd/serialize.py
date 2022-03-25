import numpy as np
import json

def serialize_array(ar, key):
    ar = ar.tolist()
    param = {key: ar}
    ar = json.dumps(param)
    return ar

def deserialize_array(serialized_array, key):
    ar = json.loads(serialized_array)[key]
    ar = np.array(ar)
    return ar

if __name__ == '__main__':
    b = np.array([[1,2,3], [1,2,3]])
    ser = serialize_array(b, 'name')
    ar = deserialize_array(ser, 'name')