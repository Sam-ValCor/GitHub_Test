#Python map function base in map from Arduino

# value = x The number to map
# fromLow = in_min the lower bound of the value's current range
# fromHigh = in_max ...
# toLow = out_min the lower bound of the value's target range.
# toHigh = out_max ...
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

"""
# test
y = _map(10, 1, 50, 50, 1)
print(y)
"""