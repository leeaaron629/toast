import unittest
from toast.git_operations import GitOperations

class TestGitOperations(unittest.TestCase):
    def setUp(self):
        self.git_ops = GitOperations()

    def test_initialization(self):
        self.assertIsNotNone(self.git_ops)
        self.assertTrue(isinstance(self.git_ops, GitOperations))

if __name__ == '__main__':
    unittest.main()
