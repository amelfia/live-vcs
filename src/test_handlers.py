import unittest
import tempfile
import os
import shutil
from unittest.mock import patch

from handlers import branch_handler, switch_handler, load_handler
from load_json import load_json, save_json


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.json = os.path.join(self.dir, "snapshot_hashes.json")
        save_json({"pointer": "main" ,
                   "snapshots": [{"branch": "main", "children": [
                   {"hash": "aaa1111", "timestamp": "time", "annotation": "somethinglol"}]}]},
                  self.json)

    def tearDown(self):
        shutil.rmtree(self.dir)



    def test_branch_handler(self):
        branch_handler(self.json, "new_prd")
        data = load_json(self.json)
        

        real = False
        for branch in data["snapshots"]:
            if branch["branch"] == "new_prd":
                real = True
            
        self.assertTrue(real)
        self.assertEqual(data["pointer"], "new_prd")

    def test_branch_handler_counter_eq(self):
        branch_handler(self.json, "main")
        data = load_json(self.json)

        counter = 0
        for branch in data["snapshots"]:
            if branch["branch"] == "main":
                counter += 1 

        self.assertEqual(counter, 1)


    def test_switch_handler_eq(self):
        switch_handler(self.json, "heheh_fake")
        self.assertEqual(load_json(self.json)["pointer"], "main")


    @patch("handlers.project_loader")
    @patch("handlers.safe_input", return_value="aaa1111")
    def test_load_handler_restores_file_and_switches_branch(self, mock_input, mock_loader):
        root_path = os.path.join(self.dir, "song.als")
        with open(root_path, "w") as f:
            f.write("root_content")

        snapshot_dir = os.path.join(self.dir, "snapshots")
        os.makedirs(snapshot_dir)
        snap_path = os.path.join(snapshot_dir, "song[t][aaa1111].als")
        with open(snap_path, "w") as f:
            f.write("snapshot_content")

        load_handler(self.json, snapshot_dir)

        with open(root_path, "r") as f:
            self.assertEqual(f.read(), "snapshot_content")
        mock_loader.assert_called_once_with(root_path)

if __name__ == "__main__":
    unittest.main()

