## KeyValueDataStore
KeyValueDataStore is a Python library which is a file based __*key-value datastore*__ that supports CRD OPERATIONS. This data store is meant to local storage.

[src.py](https://github.com/Bharath-Deva/bharathdeva/blob/master/src.py) source file for the library.

[unit_test.py](https://github.com/Bharath-Deva/bharathdeva/blob/master/unit_test.py) unit testing file for the library.

### Business Marks
- It can be initialized using an optional file path. If file path is not provided, it will reliably create itself in a corresponding location on the laptop.

- A new key-value pair can be added to the data store using the Create operation. The key is always a string - capped at 32chars. The value is always a JSON object - capped at 16KB.

- If Create is invoked for an existing key, an appropriate error must be returned.

- A Read operation on a key can be performed by providing the key, and receiving the value in response, as a JSON object.

- A Delete operation can be performed by providing the key.

- Every key supports setting a Time-To-Live property when it is created. This property is optional. If provided, it will be evaluated as an integer defining the number of seconds the key must be retained in the data store. Once the Time-To-Live for a key has expired, the key will no longer be available for Read or Delete operations.

- Appropriate error responses must always be returned to a client if it uses the data store in unexpected ways or breaches any limits.

- The file size never exceeds 1GB.

- Thread safety is implemented for the file handling. Thus it supports multi-threading.

### About the library
__Language Used__ : Python 3.9 and above
__OS__ : OS independent

#### Getting-Started
1. Clone the repo
```sh
https://github.com/Bharath-Deva/key_value_data_set.git
```

2. Install the latest version of [Python and PIP](https://www.python.org/downloads/) and set environmental path(if required)


3. Install testfixtures package for unit testing
```sh
pip install testfixtures
python unit_test.py
```


### Documentation

Import KeyValueDataSet class from [src.py](https://github.com/Bharath-Deva/bharathdeva/blob/master/src.py) and create the instance of the class for using the library.
```python
from src import KeyValueDataSet
obj = KeyValueDataSet()
```

__KeyValueDataSet([file_location])__
    Initiating will create file for data-store.
    *[file_location]* Absolute path of the file to store the data-set. Even if the path doesn't exist, it will create necessary dir and the final file.

    *NOTE* By default it creates the data-set file where src.py file is stored. And the data stored will always be type of JSON.

__KeyValueDataSet.create(data,[ttl])__
    This will append the user-data to the respected data-set file.
    *data* Data should always be of type dictionary.
    *[ttl]* It is the time-to-live property provided only in seconds and of type __int__.
    returns None.

__KeyValueDataSet.read(key)__
    Return the values to the respected key provided.
    *key* key of the value which they in need of.
    return type is of dict.

__KeyValueDataSet.delete(key)__
    Delete the key-value pair respected to the key provided.
    *key* key of the value which they want to delete.
    return None.

### Acknowledgement
1. [Python Documentaion](https://docs.python.org/3/)
