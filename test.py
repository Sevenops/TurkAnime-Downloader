import unittest
from turkanime import TurkAnime


class TestSum(unittest.TestCase):

    def test_animeler(self):
        t = TurkAnime()
        animeler = t.anime_ara("naruto")
        self.assertTrue(animeler, None)

    def test_bolumler(self):
        t = TurkAnime()
        animeler = t.anime_ara("naruto")
        bolumler = t.bolumler(animeler[0][1])
        self.assertTrue(bolumler, None)


if __name__ == "__main__":
    unittest.main()
