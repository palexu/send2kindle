import unittest
import sys

sys.path.append("../")
from sender import Sql


class ReadedDaoTest(unittest.TestCase):
    def setUp(self):
        self.dao = Sql.ReadedDao()
        self.name = "_test_nove"
        self.dao.add_novel(self.name)

    def tearDown(self):
        self.dao.del_novel(self.name)

    def test_load(self):
        novel = self.dao.load_novel(self.name)
        print(novel)
        self.assertTrue(novel[0] > 0)

    def test_is_book_exits(self):
        self.assertTrue(self.dao.is_book_exits(self.name))
        self.assertFalse(self.dao.is_book_exits("aflkj..sfef89"))

    def test_load_read_at(self):
        self.assertEqual("", self.dao.load_read_at(self.name))

    def test_set_read_at(self):
        at = "第100章"
        self.dao.set_read_at(self.name, at)
        self.assertEqual(at, self.dao.load_read_at(self.name))


class ChapterDaoTest(unittest.TestCase):
    def setUp(self):
        self.dao = Sql.ChapterDao()
        self.name = "_testChapter"
        self.title = "100"
        self.dao.add_chapter(self.name, self.title)

    def tearDown(self):
        self.dao.delete_chapter(self.name, self.title)

    def test_has_chapter(self):
        self.assertTrue(self.dao.has_chapter(self.name, self.title))
        self.assertFalse(self.dao.has_chapter(self.name, "sldkfjowihf"))
        self.assertFalse(self.dao.has_chapter("sflkjwefoi", self.title))


if __name__ == '__main__':
    unittest.main()
