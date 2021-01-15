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
        
        x1 = [x for _,x in sorted(zip(tags, x1))]
        x2 = [x for _,x in sorted(zip(tags, x2))]
        p1 = [x for _,x in sorted(zip(tags, p1))]
        p2 = [x for _,x in sorted(zip(tags, p2))]
        p3 = [x for _,x in sorted(zip(tags, p3))]
        tags = [x for _,x in sorted(zip(tags, tags))]

        part_data = np.array([x1, x2, p1, p2, p3, tags]).transpose()
        return part_data




def open_file_id(id_f):
    id_s = str(id_f).zfil(6)
    path_events = "data/EVENTS/electrons/events-{}.h5".format(id_s) 
    path_electr = "data/RAW/electrons/RAW-electrons-{}.h5".format(id_s) 
    path_photon = "data/RAW/photons/RAW-photons-{}.h5".format(id_s) 

    raw_data_e = open_raw(path_electr)
    raw_data_p = open_raw(path_photon)



