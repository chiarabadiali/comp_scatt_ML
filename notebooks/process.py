import h5py
import numpy as np
import os
import random
import progressbar

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
    id_event = str(id_f).zfill(6)
    id_raw = str(id_f-1).zfill(6)
    path_events = "raw/EVENTS/electrons/events-{}.h5".format(id_event) 
    path_electr = "raw/RAW/electrons/RAW-electrons-{}.h5".format(id_raw) 
    path_photon = "raw/RAW/photons/RAW-photons-{}.h5".format(id_raw) 

    raw_data_e = open_raw(path_electr)
    raw_data_p = open_raw(path_photon)
    events_data = open_events(path_events)

    events_final = []
    events_tags = []
    
    for row in events_data:
        if np.array_equal(np.array(row), np.array([0, 0, 0, 0, 0, 0, 0, 0])):
            pass
        else:
            tage = int(row[0]-1)
            tagp = int(row[4]-1)
            events_tags.append([tage, tagp])
            events_final.append([raw_data_e[tage][0], raw_data_e[tage][1], raw_data_e[tage][2], #3-momentum of electrons pre
                                raw_data_p[tagp][0], raw_data_p[tagp][1], raw_data_p[tagp][2], #3-momentum of photons pre
                                raw_data_e[tage][3], raw_data_e[tage][4],                      #position electron pre
                                raw_data_p[tagp][3], raw_data_p[tagp][4],                      #position photons pre
                                row[1], row[2],row[3],                                         #3-momentum of electrons post
                                row[5], row[6],row[7]]                                         #3-momentum of photons post
                                )

    events_final = np.array(events_final)
    events_tags = np.array(events_tags)
    return raw_data_e, raw_data_p, events_final , events_tags
        

def interacted(raw_data, events_tags):
    interaction = []
    n_interaction = []
    for tag, particle in enumerate(raw_data):
        if tag in events_tags:
            interaction.append(particle)
        else:
            n_interaction.append(particle)
    return interaction, n_interaction


def find_nearby(particle_set, x1, x2, dx):
    neigbours = []
    for particle in particle_set:
        if abs(particle[3] - x1) <= dx:
            if abs(particle[4] - x2) <= dx:
                neigbours.append(particle)
    return neigbours


def fake_pairs(raw_data_e, raw_data_p, events_tags, randomness, dx, N, allow_int_with_notint=False):
    int_elec, n_int_elec = interacted(raw_data_e, events_tags[:, 0])
    int_phot, n_int_phot = interacted(raw_data_p, events_tags[:, 1])

    n_rand = N*randomness
    pairs = []
    for i in range(N):
        if i <= n_rand:
            electron1 = random.choice(n_int_elec)
            neigbours_photons = find_nearby(n_int_phot, electron1[3], electron1[4], dx)
            photon_pair = random.choice(neigbours_photons)
            pairs.append([electron1[0], electron1[1], electron1[2],         #electron 3p
                          photon_pair[0], photon_pair[1], photon_pair[2],   #photon   3p
                          electron1[3], electron1[4],                       #electron 2x
                          photon_pair[3], photon_pair[4]])                  #photon   2x
        else:
            pass

    pairs = np.array(pairs) 
    return pairs



def load_generate_data(dx, file_n, r=1):
    pairs_classifier = []
    data_regression = []
    bar = progressbar.ProgressBar(maxval=file_n,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ',
                                       progressbar.Percentage(),
                                       " of {0}".format(file_n)])
    bar.start()
    for i in range(1, file_n):
        electron_raw, photon_raw, events, events_tags = open_file_id(i)
        no_pairs = fake_pairs(electron_raw, photon_raw, events_tags, r, dx, N=len(events_tags))
        yes_pairs = events[:, :10]
        for event in events:
            data_regression.append(event)
        for data_row in no_pairs:
            pairs_classifier.append(np.insert(data_row, 0, 0))
        for data_row in yes_pairs:
            pairs_classifier.append(np.insert(data_row, 0, 1))
        savedata(np.array(data_regression) ,"raw_data_regr.csv")
        savedata(np.array(pairs_classifier), "raw_data_clas.csv")
        bar.update(i)
    data_regression = np.array(data_regression)
    pairs_classifier= np.array(pairs_classifier)
    bar.finish()

    return data_regression, pairs_classifier


def savedata(data_save, name):
    np.savetxt(name, data_save, delimiter=',')

def loaddata(name):
    return np.loadtxt(name, delimiter=',')
        



