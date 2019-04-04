# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 16:35:33 2016

@author: davide
"""
import numpy as np
import h5py
import collections
from natsort import natsorted

def read_dataset( path_to_dataset ):
    """Read a preprocessed dataset.
    Dataset is expected to have the following structure:
    behavior
        linear_position
        time
        speed
    ephys
        <sensor_name1>
            spikes
                times
                amplitudes
        <sensor_name2>
            spikes
                times
                amplitudes
    
    Parameters
    ----------
    path_to_dataset : string
        full path to hdf5 file
        
    Returns
    -------
    behavior : dictionary
        pre-processed behavioral data (keys: linear_position, time, speed,
        pixel_to_cm, added_distance_pixel, n_tracks);
        items of each key are 1D array of the same length
    ephys :  ordered dictionary
        pre-processed electrophysiological data with the following keys:
            <sensor_name1>
                spike_amplitudes ( n_spikes x n_features 2d array)
                spike_times (1d array)
            <sensor_name2>
                spike_amplitudes
                spike_times
    start_stop : 2-el array
        starting and stopping time of the dataset (from event file)
        
    """
    f = h5py.File( path_to_dataset, "r" )
    
    behavior = {}
    ephys = collections.OrderedDict()
    
    start_stop = np.array( [f["general/start_time"][0], f["general/stop_time"][0]] )    
    
    dset = f["behavior"]["linear_position"]
    behavior["linear_position"] = np.zeros( len(dset) )
    dset.read_direct( behavior["linear_position"], np.s_[:], np.s_[:] )
    
    dset = f["behavior"]["time"]
    behavior["time"] = np.zeros( len(dset) )
    dset.read_direct( behavior["time"], np.s_[:], np.s_[:] )    
    
    dset = f["behavior"]["speed"]
    behavior["speed"] = np.zeros( len(dset) )
    dset.read_direct( behavior["speed"], np.s_[:], np.s_[:] )
    
    tt_ids = natsorted( f["ephys"].keys() )
    
    for tt_key in tt_ids:
        
        ephys[tt_key] = {}
        ephys[tt_key]["spike_amplitudes"] = np.zeros( f["ephys"][tt_key]["spikes"]["amplitudes"].shape )
        ephys[tt_key]["spike_times"] = np.zeros( len(f["ephys"][tt_key]["spikes"]["times"]) )
        dset = f["ephys"][tt_key]["spikes"]["amplitudes"]
        dset.read_direct( ephys[tt_key]["spike_amplitudes"], np.s_[:], np.s_[:] )
        dset = f["ephys"][tt_key]["spikes"]["times"]
        dset.read_direct( ephys[tt_key]["spike_times"], np.s_[:], np.s_[:] )
        
    return behavior, ephys, start_stop
    
    
def check_ephys_dataset( dataset, nlow=10 ):
    """Check loaded dataset of preprocessed ephys data
    
    Parameters
    ----------
    dataset : opened hdf5 file
        contains the pre-processed ephys data with the following structure
        <sensor_name1>
            spikes
                times
                amplitudes
        <sensor_name2>
            spikes
                times
                amplitudes
    nlow : int
        min number of spikes expected per each sensor of the dataset
        
    Returns
    -------
    none
    
    """
    for i, _ in enumerate(dataset):
        key = dataset.keys()[i]
        n_spikes = len(dataset[key]["spike_times"])
        if ( n_spikes != np.shape( dataset[key]["spike_times"])[0] ):
            raise ValueError(\
                "Loaded dataset has inconsistent number of spikes. Check " + key )
        if ( n_spikes < nlow ):
            raise ValueError("Detected tetrode with very low number of spikes." +\
            "Make sure dataset was created correctly.")

            
# -*- coding: utf-8 -*-
# -*- mode: python -*-
"""
Code to get data
"""
def read_neuron(partition):
    data_neuron=[]
    import glob
    from zipfile import ZipFile 
    import numpy as np
    if (partition=="all"):
        for name in glob.glob('data/*.zip'): 
            with ZipFile(name, 'r') as zip: 
                zip.extractall('data/unzippedfiles')
            for name in glob.glob('data/unzippedfiles/*.hdf5'):
                file=read_dataset(name)
                data_neuron.append(file[1])          
        Day1={'first run':data_neuron[0],
              'rest':data_neuron[2],
              'second run':data_neuron[1]}
        Day2={'first run':data_neuron[4],
              'rest':data_neuron[5],
              'second run':data_neuron[3]}
        Day3={'first run':data_neuron[7],
              'rest':data_neuron[8],
              'second run':data_neuron[6]}
        neuron_dict_all={'Day':{'08/23/2017':Day1,
                     '08/24/2017':Day2,
                     '08/25/2017':Day3}} 
        np.save('data/neuron_dict_all.npy', neuron_dict_all)
    elif (partition=="day1"):
        for name in glob.glob('data/2017-08-23*.zip'): 
            with ZipFile(name, 'r') as zip: 
                zip.extractall('data/unzippedfiles')
            for name in glob.glob('data/unzippedfiles/*.hdf5'):
                file=read_dataset(name)
                data_neuron.append(file[1])
        Day1={'first run':data_neuron[0],
              'rest':data_neuron[2],
              'second run':data_neuron[1]}
        np.save('data/neuron_dict_day1.npy',Day1)   
    elif (partition=="day2"):
        for name in glob.glob('data/2017-08-24*.zip'): 
            with ZipFile(name, 'r') as zip: 
                zip.extractall('data/unzippedfiles')
            for name in glob.glob('data/unzippedfiles/*.hdf5'):
                file=read_dataset(name)
                data_neuron.append(file[1])
        Day2={'first run':data_neuron[0],
              'rest':data_neuron[2],
              'second run':data_neuron[1]}
        np.save('data/neuron_dict_day2.npy',Day2)  
    elif (partition=="day3"):
        for name in glob.glob('data/2017-08-25*.zip'): 
            with ZipFile(name, 'r') as zip: 
                zip.extractall('data/unzippedfiles')
            for name in glob.glob('data/unzippedfiles/*.hdf5'):
                file=read_dataset(name)
                data_neuron.append(file[1])
        Day3={'first run':data_neuron[0],
              'rest':data_neuron[2],
              'second run':data_neuron[1]}
        np.save('data/neuron_dict_day3.npy',Day3)
    else:
        print("Incorrect Arguement Input, Try: all, day1, day2, day3")
