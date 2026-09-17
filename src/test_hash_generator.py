import unittest
import os
import gzip
import tempfile
import shutil
from hash_generator import hash_generator


class TestHashGenerator(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.dir)



    def make_als(self, name, value):
        path = os.path.join(self.dir, name)
        with gzip.open(path, "wb") as f:
            f.write(value)
        return path


    def test_file_doesnt_exist_true(self):
        result = hash_generator(os.path.join(self.dir, "type.als"))
        self.assertIsNone(result)

    def test_hash_generator_eq(self):
        result1 = self.make_als("fake1.als", b"<Ableton>same</Ableton>")
        result2 = self.make_als("fake2.als", b"<Ableton>same</Ableton>")
        self.assertEqual(hash_generator(result1), hash_generator(result2))

    def test_hash_generator_not_eq(self):
        result1 = self.make_als("fake1.als", b"<Ableton>not_same</Ableton>")
        result2 = self.make_als("fake2.als", b"Ableton>hehe_not_same</Ableton>")
        self.assertNotEqual(hash_generator(result1), hash_generator(result2))

if __name__ == "__main__":
    unittest.main()
