import unittest
from testfixtures import tempdir, compare
from src import KeyValueDataSet
import os
import json


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
    def test_file_creation(self,dir):
        print('testing file creation')
        path1 = os.path.join(dir.path,'test.txt')
        obj1 = KeyValueDataSet(path1)
        obj2 = KeyValueDataSet()
        path2 = os.path.join(os.getcwd(),'data.json')
        if not (os.path.exists(path1)):
            raise Exception('failed : optimal path')
        if not (os.path.exists(path2)):
            raise Exception('failed : default path')

    @tempdir()
    def test_create_fun(self,dir):
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
    def test_read_fun(self,dir):
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