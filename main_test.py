import unittest
from main import read_file


class TestReadFile(unittest.TestCase):

    def test_read_file(self):
        symbols_dict, nodes_list, edges_list = read_file("ped")

        expected_symbols_dict = {1: 'symbol1', 2: 'symbol2', 3: 'symbol3'}
        expected_nodes_list = ['node1', 'node2', 'node3']
        expected_edges_list = ['1;2;3;4;5;6;7', '2;3;4;5;6;7;8', '3;4;5;6;7;8;9']

        self.assertEqual(symbols_dict, expected_symbols_dict)
        self.assertEqual(nodes_list, expected_nodes_list)
        self.assertEqual(edges_list, expected_edges_list)

if __name__ == '__main__':
    unittest.main()
