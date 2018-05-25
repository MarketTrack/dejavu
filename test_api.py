import requests
import json
import zlib
from scipy.io import wavfile
from pprint import pprint

filename = 'C:\\src\\data\\rumpel\\test_16000.wav'
sample_rate, data = wavfile.read(filename)

def fingerprint_file():
    # segment_len_seconds = 15
    # offset_from_start_seconds = 6
    
    # start = int(sample_rate*offset_from_start_seconds)
    # end = int(start + sample_rate*segment_len_seconds)
    # data = data[start:end]

    dict_payload = {}
    dict_payload['name'] = filename
    dict_payload['sample_rate'] = sample_rate
    dict_payload['wav_data'] = data.tolist()

    payload = zlib.compress(json.dumps(dict_payload).encode('utf-8'))
    response = requests.post('http://127.0.0.1:5000/fingerprintaudio', data=payload)
    pprint(response.content)

def recognize_file_segment():
    segment_len_seconds = 5
    offset_from_start_seconds = 7
    
    start = int(sample_rate*offset_from_start_seconds)
    end = int(start + sample_rate*segment_len_seconds)
    wav_segment = data[start:end]

    dict_payload = {}
    dict_payload['sample_rate'] = sample_rate
    dict_payload['wav_data'] = wav_segment.tolist()

    payload = zlib.compress(json.dumps(dict_payload).encode('utf-8'))
    response = requests.post('http://127.0.0.1:5000/recognize', data=payload)
    from pprint import pprint
    pprint(response.content)

#fingerprint_file()
recognize_file_segment()