import json
import sys
import os
import threading

class key_value_data_set:
    def __init__(self, file_path = 'data.json'):
        self.lock = threading.Lock()
        try:
            if(file_path == 'data.json'): 
                self.file_location = file_path 
                self.open_file()
            else:
                self.file_location = file_path
                file_path = os.path.dirname(file_path)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                if not os.path.isfile(self.file_location):
                    self.open_file()
        except OSError:
            raise OSError('ERROR : Path is not valid')

    def open_file(self):
        with open(self.file_location, 'w') as f:
            data = {}
            json.dump(data,f)


    def is_key_value_pair_legitimate(self, key, value, file_data):
        if(key in file_data):
            raise Exception(f'ERROR : Your key {key} is already registered. Try some unique keys')
        if( len(key)>32):
            raise Exception(f'ERROR : Key {key} is of length more than 32 character')
        if(not key.isalpha()):
            raise Exception(f'ERROR : Key {key} is not of alphabatics (May conatin numbers or spaces or special character)')
        if(sys.getsizeof(value)>16384):
            raise Exception(f"ERROR : Your value {value} size is exceeding 16KB (Your value's is {sys.getsizeof(value)})")
        if(not isinstance(value,dict)):
            raise Exception('ERROR : Value is not of JSON')
        
    def checking_file_size(self, file_path):
        size = (os.stat(file_path).st_size)/(1024*1024)
        if size < 1024:
            return 0
        return 1

    def time_to_live(self,ttl,key):
        pass


    def create(self, data, ttl = False):
        with self.lock:
            if(self.checking_file_size(self.file_location)):
                raise Exception('ERROR : File size is exceeding 1GB')
            key,value = list(data.items())[0]
            if(ttl):
                self.time_to_live(ttl,key)
            with open(self.file_location, 'r+') as f:
                file_data = json.load(f)
                self.is_key_value_pair_legitimate(key, value, file_data) 
                file_data.update(data)
                f.seek(0)
                json.dump(file_data,f)
                return(None)
    
    def read(self, provided_key):
        with open(self.file_location, 'r') as f:
            file_data = json.load(f)
            if(provided_key in file_data):
                return(file_data[provided_key])
            else:
                raise Exception(f"ERROR : provided key {provided_key} isn't in the data-set")

    def delete(self, provided_key):
        with self.lock:
            with open(self.file_location, 'r+') as f:
                file_data = json.load(f)
                if(provided_key in file_data):
                    del(file_data[provided_key])
                    f.seek(0)
                    f.truncate()
                    json.dump(file_data,f)
                    return(None)
                else:
                    raise Exception(f"ERROR : provided key {provided_key} isn't in the data-set")
