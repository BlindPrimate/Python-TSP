import unittest
from datamodel.hashtable import HashTable


class MyTestCase(unittest.TestCase):

    def test_length(self):
        test = HashTable(4)
        self.assertEqual(len(test.array), 4, "Table should be appropriate size")
        self.assertNotEqual(len(test.array), 10)

    def test_find(self):
        test = HashTable(5)
        test.insert(5383)
        self.assertEqual(test.find(5383), 5383)

    def test_remove(self):
        test = HashTable(5)
        test.insert(11214)
        test.insert(8888)
        test.remove(8888)
        self.assertIs(test.find(8888), None)

    def test_length(self):
        test = HashTable(5)
        test.insert(11214)
        test.insert(8888)
        self.assertEqual(len(test), 2)
        test.remove(8888)
        self.assertEqual(len(test), 1)

if __name__ == '__main__':
    unittest.main()
