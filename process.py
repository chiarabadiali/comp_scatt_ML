import h5py
import numpy as np

def open_raw(filepath):
    with h5py.File(filepath,'r') as f:
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

        part_data = np.array([p1, p2, p3, x1, x2, tags]).transpose()
        return part_data


def open_events(filepath):
    with h5py.File(filepath,'r') as f:
        data = list(f["events"])
    return data


def open_file_id(id_f):
    id_s = str(id_f).zfill(6)
    path_events = "data/EVENTS/electrons/events-{}.h5".format(id_s) 
    path_electr = "data/RAW/electrons/RAW-electrons-{}.h5".format(id_s) 
    path_photon = "data/RAW/photons/RAW-photons-{}.h5".format(id_s) 

    raw_data_e = open_raw(path_electr)
    raw_data_p = open_raw(path_photon)
    events_data = open_events(path_events)

    events_final = []
    
    for row in events_data:
        if row == [0, 0, 0, 0, 0, 0, 0, 0]:
            break
        tage = row[0]
        tagp = row[4]
        events_final.append(raw_data_e[tage][0], raw_data_e[tage][1], raw_data_e[tage][2], #3-momentum of electrons pre
                            raw_data_p[tagp][0], raw_data_p[tagp][1], raw_data_p[tagp][2], #3-momentum of photons pre
                            raw_data_e[tage][3], raw_data_e[tage][4],                      #position electron pre
                            raw_data_p[tagp][3], raw_data_p[tagp][4],                      #position photons pre
                            row[1], row[2],row[3],                                         #3-momentum of electrons post
                            row[5], row[6],row[7],                                         #3-momentum of photons post
                            )
    events_final = np.array(events_final)
    return events_final 
        
