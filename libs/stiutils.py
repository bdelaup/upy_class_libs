
def interpolate(val, inter_in, inter_out):
    """Remap value fron inter_in to inter_in"""
    fraction_inval = (val - inter_in[0]) / (inter_in[1] - inter_in[0])
    fraction_outval = fraction_inval * (inter_out[1] - inter_out[0])
    offset_out = inter_out[0]
    val_out = offset_out + fraction_outval
    return val_out

def tests():
    assert interpolate(12, [10, 20], [10, 40]) == 16
    assert interpolate(12, [10, 20], [20, 40]) == 24
    assert interpolate(15, [10, 20], [0, 40]) == 20
    print("SUCCESS")
    
if __name__ == "__main__":
    tests()