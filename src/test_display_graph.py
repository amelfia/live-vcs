import unittest
from display_graph import(
    forked_from_hash,
    render_graph
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


class TestDisplayGraph(unittest.TestCase):
    
    def test_fork_hash_eq(self):
        data = fake_data()
        result = forked_from_hash(data)
        self.assertEqual(result, {"aaa1111": ["new_slice"]})
    
    def test_no_fork_eq(self):
        data = {"pointer": "main",
                "snapshots": [{"branch": "main", "children": [ 
                {"hash": "aaa1111", "annotation": "o"}]}]}
        self.assertEqual(forked_from_hash(data), {})



    def test_render_graph_in(self):
        data = fake_data()
        result = render_graph(data)
        commits = ("aaa1111", "bbb2222", "ccc3333")

        for commit in commits:
            self.assertIn(commit[:7], result)

    def test_branch_tip_in(self):
        data = fake_data()
        result = render_graph(data)
        self.assertIn("(new_slice)", result)
        
    def test_main_tip_notIn(self):
        data = fake_data()
        result = render_graph(data)
        self.assertNotIn("(main)", result)

        
if __name__ == "__main__":
    unittest.main()
