import unittest
from branch import (
    get_branch,
    parent_hash_of_branch,
    create_branch,
    switch_branch,
    current_branch,
    find_branch_by_commit_hash
)

def fake_data():
    return {
        "pointer": "main",
        "snapshots": [
            {"branch": "main", "children": [
                {"hash": "aaa1111", "timestamp": "t1", "annotation": "init"},
                {"hash": "bbb2222", "timestamp": "t2", "annotation": "drums"},
            ]},
            {"branch": "new_slice",
                "branched_from": {"branch": "main", "hash": "aaa1111"},
                "children": [
                {"hash": "ccc3333", "timestamp": "t3", "annotation": "synth"},
            ]},
        ],
        }

class TestBranch(unittest.TestCase):

    def test_get_branch_eq(self):
        data = fake_data()
        branch = get_branch(data, "new_slice")
        self.assertEqual(branch["branch"], "new_slice")
    
    def test_get_branch_none(self):
        data = fake_data()
        self.assertIsNone(get_branch(data, "should_return_none"))
        

    def test_parent_hash_eq(self):
        data = fake_data()
        result = get_branch(data, "main")
        self.assertEqual(parent_hash_of_branch(result), "bbb2222")

    def test_parent_hash_none(self):
        fake_dict = {"branch": "new_synth", "children": []}
        self.assertIsNone(parent_hash_of_branch(fake_dict))

    def test_create_branch_length_eq(self):
        data = fake_data()
        result = len(data["snapshots"])
        create_branch(data, "synthl", "main", "bbb2222")
        self.assertEqual(len(data["snapshots"]), result + 1)

    def test_create_branch_reference_eq(self):
        data = fake_data()
        create_branch(data, "synthl", "main", "bbb2222")
        result = get_branch(data, "synthl")
        self.assertEqual(result["branched_from"]["hash"],"bbb2222")
        self.assertEqual(result["children"], [])

    def test_switch_branch_eq(self):
        data = fake_data()
        switch_branch(data, "new_slice")
        self.assertEqual(data["pointer"], "new_slice")

    def test_switch_fake_branch(self):
        data = fake_data()
        with self.assertRaises(ValueError):
            switch_branch(data, "fake_branch")

    def test_current_branch_pointer_eq(self):
        data = fake_data()
        data["pointer"] = "new_slice"
        self.assertEqual(current_branch(data)["branch"], "new_slice")

    def test_random_pointer_raises_error(self):
        data = fake_data()
        data["pointer"] = "i am deleted"
        with self.assertRaises(ValueError):
            current_branch(data)

    def test_find_branch_by_commit_hash(self):
        data = fake_data()
        self.assertEqual(find_branch_by_commit_hash(data, "ccc3333"), "new_slice")
        self.assertEqual(find_branch_by_commit_hash(data, "aaa1111"), "main")
        self.assertIsNone(find_branch_by_commit_hash(data, "unknown"))

if __name__ == "__main__":
   unittest.main()
