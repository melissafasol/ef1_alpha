import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import scipy
from scipy.signal import decimate
import mne
import glob
import re

NUM_HEADER_BYTES = 1024
SAMPLES_PER_RECORD = 1024
BYTES_PER_SAMPLE = 2
RECORD_SIZE = 4 + 8 + SAMPLES_PER_RECORD * BYTES_PER_SAMPLE + 10


def regex_capture(pattern, list_of_strings, take_index=0):
    """Apply regex `pattern` to each string and return a captured group.
    
    pattern : string, regex pattern
    list_of_strings : list of strings to apply the pattern to
        Strings that do not match the pattern are ignored.
    take_index : The index of the captured group to return
    
    Returns: a list of strings. Each element is the captured group from
        one of the input strings.
    """
    res_l = []
    for s in list_of_strings:
        m = re.match(pattern, s)
        
        # Append the capture, if any
        if m is not None:
            res_l.append(m.groups()[take_index])
    
    return res_l

def _get_sorted_channels(folderpath, recording=None):
    """Return a sorted list of the continuous channels in folderpath.
    
    folderpath : string, path to location of continuous files on disk
    recording : None, or int
        If there is only one recording in the folder, leave as None.
        Otherwise, specify the number of the recording as an integer.
    """
    if recording is None:
        return sorted([int(f.split('_CH')[1].split('.')[0]) for f in os.listdir(folderpath) 
                    if '.continuous' in f and '_CH' in f]) 
    else:
        # Form a string from the recording number
        if recording == 1:
            # The first recording has no suffix
            recording_s = ''
        else:
            recording_s = '_%d' % recording
        
        # Form a regex pattern to be applied to each filename
        # We will capture the channel number: (\d+)
        regex_pattern = '%s_CH(\d+)%s.continuous' % ('100', recording_s)
        
        # Apply the pattern to each filename and return the captured channels
        channel_numbers_s = regex_capture(regex_pattern, os.listdir(folderpath))
        channel_numbers_int = map(int, channel_numbers_s)
        return sorted(channel_numbers_int)

def loadContinuous(filepath, dtype = float):

    assert dtype in (float, np.int16), \
      'Invalid data type specified for loadContinous, valid types are float and np.int16'

    print("Loading continuous data...")

    ch = { }

    #read in the data
    f = open(filepath,'rb')

    fileLength = os.fstat(f.fileno()).st_size

    # calculate number of samples
    recordBytes = fileLength - NUM_HEADER_BYTES
    if  recordBytes % RECORD_SIZE != 0:
        raise Exception("File size is not consistent with a continuous file: may be corrupt")
    nrec = recordBytes // RECORD_SIZE
    nsamp = nrec * SAMPLES_PER_RECORD
    # pre-allocate samples
    samples = np.zeros(nsamp, dtype)
    timestamps = np.zeros(nrec)
    recordingNumbers = np.zeros(nrec)
    indices = np.arange(0, nsamp + 1, SAMPLES_PER_RECORD, np.dtype(np.int64))

    header = readHeader(f)

    recIndices = np.arange(0, nrec)

    for recordNumber in recIndices:

        timestamps[recordNumber] = np.fromfile(f,np.dtype('<i8'),1) # little-endian 64-bit signed integer
        N = np.fromfile(f,np.dtype('<u2'),1)[0] # little-endian 16-bit unsigned integer

        #print index

        if N != SAMPLES_PER_RECORD:
            raise Exception('Found corrupted record in block ' + str(recordNumber))

        recordingNumbers[recordNumber] = (np.fromfile(f,np.dtype('>u2'),1)) # big-endian 16-bit unsigned integer

        if dtype == float: # Convert data to float array and convert bits to voltage.
            data = np.fromfile(f,np.dtype('>i2'),N) * float(header['bitVolts']) # big-endian 16-bit signed integer, multiplied by bitVolts
        else:  # Keep data in signed 16 bit integer format.
            data = np.fromfile(f,np.dtype('>i2'),N)  # big-endian 16-bit signed integer
        samples[indices[recordNumber]:indices[recordNumber+1]] = data

        marker = f.read(10) # dump

    #print recordNumber
    #print index

    ch['header'] = header
    ch['timestamps'] = timestamps
    ch['data'] = samples  # OR use downsample(samples,1), to save space
    ch['recordingNumber'] = recordingNumbers
    f.close()
    return ch

def loadFolderToArray(folderpath, channels = 'all', chprefix = 'CH',
                      dtype = float, session = '0', source = '100'):
    '''Load continuous files in specified folder to a single numpy array. By default all
    CH continous files are loaded in numerical order, ordering can be specified with
    optional channels argument which should be a list of channel numbers.'''

    if channels == 'all':
        channels = _get_sorted_channels(folderpath, chprefix, session, source)

    if session == '0':
        filelist = [source + '_'+chprefix + x + '.continuous' for x in map(str,channels)]
    else:
        filelist = [source + '_'+chprefix + x + '_' + session + '.continuous' for x in map(str,channels)]

    numFiles = 1

    channel_1_data = loadContinuous(os.path.join(folderpath, filelist[0]), dtype)['data']

    n_samples  = len(channel_1_data)
    n_channels = len(filelist)

    data_array = np.zeros([n_samples, n_channels], dtype)
    data_array[:,0] = channel_1_data

    for i, f in enumerate(filelist[1:]):
            data_array[:, i + 1] = loadContinuous(os.path.join(folderpath, f), dtype)['data']
            numFiles += 1

    return data_array

def readHeader(f):
    header = { }
    h = f.read(1024).decode().replace('\n','').replace('header.','')
    for i,item in enumerate(h.split(';')):
        if '=' in item:
            header[item.split(' = ')[0]] = item.split(' = ')[1]
    return header

def downsample(trace,down):
    downsampled = scipy.signal.resample(trace,np.shape(trace)[0]/down)
    return downsampled

