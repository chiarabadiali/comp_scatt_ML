import h5py
import numpy as np

def open_raw(filepath):
    with h5py.File(filepath) as f:
        x1 = list(f["x1"])
        x2 = list(f["x2"])
        p1 = list(f["p1"])
        p2 = list(f["p2"])
        p3 = list(f["p3"])
        tags = list(np.array(list(f["tag"]))[:, 1])
    return x1, x2, p1, p2, p3, tags
