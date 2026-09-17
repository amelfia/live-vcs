import unittest
import os
import tempfile
import shutil
from snapshot import (
    snapshot,
    snapshot_dir_for_json,
    als_root_finder,
    find_snapshot
)


class TestAlsRootFinder(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.json = os.path.join(self.dir, "snapshot_hashes.json")

    def tearDown(self):
        shutil.rmtree(self.dir)



    def test_als_root_founder_true(self):
        with open(os.path.join(self.dir, "love_from.als"), "w"):
            pass
        self.assertTrue(als_root_finder(self.json).endswith("love_from.als"))


    def test_als_root_founder_more_than_one_root_IsNone(self):
        with open(os.path.join(self.dir, "fake1.als"), "w"):
            pass

        with open(os.path.join(self.dir, "fake2.als"), "w"):
            pass
        self.assertIsNone(als_root_finder(self.json))
    

    def test_als_root_founder_no_root_IsNone(self):
        self.assertIsNone(als_root_finder(self.json))

class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)


    def test_snapshot_name_true(self):
        path = os.path.join(self.dir, "techno.als")
        with open(path, "w"):
            pass
        target = snapshot(path, "3f3f3f3", self.dir, "2026-09-10T10-00-00")
        self.assertTrue(os.path.isfile(target))
        self.assertIsNotNone(find_snapshot(self.dir, "3f3f3f3"))

    def test_find_snapshot_hashing_file_name_true(self):
        name = "fake[2026-09-10T10-00-00][ccc3333].als"
        with open(os.path.join(self.dir, name), "w"):
            pass
        result = find_snapshot(self.dir, "ccc3333")
        self.assertTrue(result.endswith(name))

    def test_snapspshot_finder_isNone(self):
        self.assertIsNone(find_snapshot(self.dir, "fdfdjfdf"))
    
    def tests_snapshot_dir_eq(self):
        json_path = os.path.join(self.dir, "snapshot_hashes.json")
        result = snapshot_dir_for_json(json_path)
        self.assertEqual(result, os.path.join(self.dir, "snapshots"))
        
if __name__ == "__main__":
    unittest.main()
