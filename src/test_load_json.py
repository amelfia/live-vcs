import unittest
import os
import tempfile
import shutil
from load_json import (
    load_json,
    save_json,
    commit_structure
)


class TestLoadJson(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.json = os.path.join(self.dir, "snapshot_hashes.json")


    def tearDown(self):
        shutil.rmtree(self.dir)



    def test_no_file_exists_eq(self):
        data = load_json(self.json)
        self.assertEqual(data["pointer"], "main")
        self.assertEqual(data["snapshots"], [{"branch": "main", "children": []}])


    def test_empty_file_structure_eq(self):
        with open(self.json, "w"):
            pass
        data = load_json(self.json)
        self.assertEqual(data["pointer"], "main")

    def test_save_and_load_eq(self):
        result = {"pointer": "new_synth", "snapshots": [{"branch": "new_synth", "children": []}]}
        save_json(result, self.json)
        self.assertEqual(load_json(self.json), result)


    


    def test_commit_structure_eq(self):
        commit = commit_structure("hhh1111", "did something", "2026-09-10T10:00:00")
        self.assertEqual(commit, {"hash": "hhh1111",
                                  "timestamp": "2026-09-10T10:00:00",
                                  "annotation": "did something"})



if __name__ == "__main__":
    unittest.main()
