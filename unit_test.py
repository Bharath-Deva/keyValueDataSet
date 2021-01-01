'''
    unit testing for src.py is done here using testfixtures library.
'''

# ------------------------------------------------------------------------

import unittest
from testfixtures import tempdir, compare
from src import KeyValueDataSet
import os
import json
import time

class TestingKeyValueDataSet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print('Testing started\n') 

    @classmethod
    def tearDownClass(self):
        print('\nTesting ended') 

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown\n')
    
    @tempdir()
    def test_user_defined_file_creation(self,dir):
        ''' after creating the instance of KeyValueDataSet checking weather
        files are created properly irrespective of path provided by the user.
        '''
        print('testing file creation')
        user_defined_path = os.path.join(dir.path,'test.txt')
        user_defined_obj = KeyValueDataSet(user_defined_path)
        if not (os.path.exists(user_defined_path)):
            raise Exception('failed : optimal path')

    @tempdir()
    def test_default_file_creation(self,dir):
        default_path = os.path.join(os.getcwd(),'data.json')
        default_obj = KeyValueDataSet()
        if not (os.path.exists(default_path)):
            raise Exception('failed : default path')

    @tempdir()
    def test_single_input_create_fun(self,dir):
        ''' checking the buisness marks and the creation of json data
        feeding into the data set file
        '''
        print('testing create function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test = {"a": {"test":"data"}}
        obj.create(test)
        compare(test , json.loads(dir.read('test.txt')))
        with self.assertRaises(Exception):
            obj.create({'error': 'vaue is not of json'})
            obj.create({'a b1':{'error':'key is not of type string'}})
            obj.create({'keyLengthGreaterThanThirtyTwoCharacter':{'error':'key size error'}})
            obj.create({'a':{'error':'key is not unique'}})

    @tempdir()
    def test_buisness_marks(self,dir):
        print('testing create function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test = {"a": {"test":"data"}}
        obj.create(test)
        with self.assertRaises(Exception):
            obj.create({'error': 'vaue is not of json'})
            obj.create({'a b1':{'error':'key is not of type string'}})
            obj.create({'keyLengthGreaterThanThirtyTwoCharacter':{'error':'key size error'}})
            obj.create({'a':{'error':'key is not unique'}})

    @tempdir()
    def test_multiple_input_create_fun(self,dir):
        print('testing multiple input for create function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test1 = {"a": {"test1":"data1"}}
        obj.create(test1) 
        compare(test1 , json.loads(dir.read('test.txt')))
        test2 = {"b": {"test2":"data2"}}
        obj.create(test2)
        test1.update(test2)
        compare(test1 , json.loads(dir.read('test.txt')))

    @tempdir()
    def test_time_to_live_property(self,dir):
        print('testing time to live function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test1 = {"a": {"test1":"data1"}}
        obj.create(test1, 5) #5 seconds is provided
        time.sleep(5)
        with self.assertRaises(Exception):
            obj.read("a")

    


    @tempdir()
    def test_read_fun(self,dir):
        ''' checking the wheather proper response is obtained from the 
        read method of src.py
        '''
        print('testing read function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test = {"a": {"test":"data"}}
        obj.create(test)
        self.assertEqual(obj.read('a'),test['a'])
        with self.assertRaises(Exception):
            obj.read("b")
        
    @tempdir()
    def test_delete_fun(self,dir):
        '''checking wheather delete operation is performed by delete method 
        with proper key value
        '''
        print('testing read function')
        path = os.path.join(dir.path,'test.txt')
        obj = KeyValueDataSet(path)
        test = {"a": {"test":"data"}}
        obj.create(test)
        obj.delete("a")
        compare({} , json.loads(dir.read('test.txt')))
        with self.assertRaises(Exception):
            obj.delete("b")

    

if __name__ == "__main__":
    unittest.main()