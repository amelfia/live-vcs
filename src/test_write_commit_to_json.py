import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
from load_json import load_json, save_json
import write_commit_to_json as wc
from write_commit_to_json import commit_duplicate, write_commit_to_json



class TestCommitDuplicate(unittest.TestCase):

    def test_is_duplicate_true(self):
        commit = {"branch": "main", "children": [{"hash": "aaa1111"}]}
        self.assertTrue(commit_duplicate(commit, "aaa1111"))

    def test_not_duplicate_false(self):
        commit = {"branch": "main", "children": [{"hash": "aaa1111"}]}
        self.assertFalse(commit_duplicate(commit, "777777"))

    def test_empty_branch_false(self):
        commit = {"branch": "main", "children": []}
        self.assertFalse(commit_duplicate(commit, "fake_1111"))




class TestWriteCommitToJson(unittest.TestCase):
    def setUp(self):
        self.dir= tempfile.mkdtemp()
        self.json = os.path.join(self.dir, "snapshot_hashes.json")

        save_json({"pointer": "main",
                   "snapshots": [{"branch": "main", "children": []}]},
                  self.json)

        self.als = os.path.join(self.dir, "fake_song.als")

        with open(self.als, "w"):
            pass

    def tearDown(self):
        shutil.rmtree(self.dir)

    @patch.object(wc, "safe_input", return_value="v1_save")
    @patch.object(wc, "hash_generator", return_value="hhh1111")
    def test_commit_equal(self, mock_hash, mock_input):
        write_commit_to_json(self.als, self.json)
        data = load_json(self.json)
        children = data["snapshots"][0]["children"]
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0]["hash"], "hhh1111")
        self.assertEqual(children[0]["annotation"], "v1_save")


    @patch.object(wc, "safe_input", return_value="something")
    @patch.object(wc, "hash_generator", return_value="hhh1111")
    def test_same_hash_no_commit_eq(self, mock_hash, mock_input):
        write_commit_to_json(self.als, self.json)
        write_commit_to_json(self.als, self.json)
        data = load_json(self.json)
        self.assertEqual(len(data["snapshots"][0]["children"]), 1)



    @patch.object(wc, "safe_input", return_value="never_asked")
    @patch.object(wc, "hash_generator", return_value=None)
    def test_writing_hash_gives_error_eq(self, mock_hash, mock_input):
        write_commit_to_json(self.als, self.json)
        data = load_json(self.json)
        self.assertEqual(len(data["snapshots"][0]["children"]), 0)
        mock_input.assert_not_called()

if __name__ == "__main__":
    unittest.main()

