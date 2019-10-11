import sys
sys.path.append("..")

import unittest
from tensorflow.keras import models
from backend.training import preprocess


class BigDigitTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.model = models.load_model("./models/digits/1/")


    def test_big_0(self):
        self.__predict_test("./images/280x280/numero0.png", 0)

    def test_big_1(self):
        self.__predict_test("./images/280x280/numero1.png", 1)

    def test_big_2(self):
        self.__predict_test("./images/280x280/numero2.png", 2)

    def test_big_3(self):
        self.__predict_test("./images/280x280/numero3.png", 3)

    def test_big_4(self):
        self.__predict_test("./images/280x280/numero4.png", 4)

    def test_big_5(self):
        self.__predict_test("./images/280x280/numero5.png", 5)

    def test_big_6(self):
        self.__predict_test("./images/280x280/numero6.png", 6)

    def test_big_7(self):
        self.__predict_test("./images/280x280/numero7.png", 7)

    def test_big_8(self):
        self.__predict_test("./images/280x280/numero8.png", 8)
        
    def test_big_9(self):
        self.__predict_test("./images/custom imagesVAL/9/9.png", 9)



    def __predict_test(self, path, expected):
        x = preprocess(path)
        prediction = self.model.predict_classes(x)[0]
        self.assertEqual(expected, prediction)