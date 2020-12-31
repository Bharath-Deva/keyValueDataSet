# This module will support key-value data store that supports CRD OPERATIONS in local computer.

#---------------------------------------------------------------------------

#     It can be initialized using an optional file path. If one is not provided, it will reliably create itself in a reasonable location on the laptop.
# 
#     A new key-value pair can be added to the data store using the Create operation. The key is always a string - capped at 32chars. The value is always a JSON object - capped at 16KB.
# 
#     If Create is invoked for an existing key, an appropriate error must be returned.
#     A Read operation on a key can be performed by providing the key, and receiving the value in response, as a JSON object.
# 
#     A Delete operation can be performed by providing the key.
# 
#     Every key supports setting a Time-To-Live property when it is created. This property is optional. If provided, it will be evaluated as an integer defining the number of seconds the key must be retained in the data store. Once the Time-To-Live for a key has expired, the key will no longer be available for Read or Delete operations.
# 
#     Appropriate error responses must always be returned to a client if it uses the data store in unexpected ways or breaches any limits
# 
#     The file size never exceeds 1GB.
# 
#     Supports thread safety. Thus it supports multi-threading



#---------------------------------------------------------------------------


import json
import sys
import os
import threading
import time

class KeyValueDataSet:
    def __init__(self, file_path = 'data.json'):
        '''
            When the class is created with instance, the constructor will create the necessary file and dir for the key-value data store
        '''
        self.lock = threading.Lock()
        try:
            if(file_path == 'data.json'): 
                self.file_location = file_path 
                self.__open_file()
            else:
                self.file_location = file_path
                file_path = os.path.dirname(file_path)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                if not os.path.isfile(self.file_location):
                    self.__open_file()
        except OSError:
            raise OSError('ERROR : Path is not valid')

    def __open_file(self):
        with open(self.file_location, 'w') as f:
            json.dump({},f)

    def __is_key_value_pair_legitimate(self, key, value, file_data):
        ''' checking weather the key and value satisfy business marks
        '''
        if(not isinstance(value,dict)):
            raise Exception('ERROR : Value is not of JSON')
        if(sys.getsizeof(value)>16384):
            raise Exception(f"ERROR : Your value {value} size is exceeding 16KB (Your value's is {sys.getsizeof(value)})")
        if(not key.isalpha()):
            raise Exception(f'ERROR : Key {key} is not of alphabatics (May conatin numbers or spaces or special character)')
        if( len(key)>32):
            raise Exception(f'ERROR : Key {key} is of length more than 32 character')
        if(key in file_data):
            raise Exception(f'ERROR : Your key {key} is already registered. Try some unique keys')
        
    def __checking_file_size(self, file_path):
        size = (os.stat(file_path).st_size)
        if size < (1024*1024*1024):
            return 0
        return 1

    def __time_to_live(self,ttl,key):
        if(not isinstance(ttl,int)):
            raise Exception('TTL operand should be of type int')
        time.sleep(ttl-0.2)
        self.delete(key)


    def create(self, req_data, ttl = False):
        with self.lock:
            if(self.__checking_file_size(self.file_location)):
                raise Exception('ERROR : File size is exceeding 1GB') 
            key,value = list(req_data.items())[0]
            if(ttl):
                threading.Thread(target=self.__time_to_live, args=(ttl,key)).start() #creating a thread for 
            with open(self.file_location, 'r+') as f:
                file_data = json.load(f)
                self.__is_key_value_pair_legitimate(key, value, file_data) 
                file_data.update(req_data)
                f.seek(0)
                f.write(json.dumps(file_data))
                return(None)
    
    def read(self, provided_key):
        with open(self.file_location, 'r') as f:
            res_file_data = json.load(f)
            if(provided_key in res_file_data):
                return(res_file_data[provided_key])
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