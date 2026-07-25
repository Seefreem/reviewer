import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtWidgets import QApplication

from main import Row3
from src.knowledgeObject import knowledgeObject


class DummyRoot:
    def __init__(self, object_list):
        self.kol = type("Kol", (), {"objectList": object_list, "mode": 0})()
        self.reviewIndex = 0

    def GoToPageX(self, page_number):
        self.reviewIndex = page_number - 1


class DeleteButtonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_delete_button_removes_current_item(self):
        first = knowledgeObject(body={"context": "first"})
        second = knowledgeObject(body={"context": "second"})
        root = DummyRoot([first, second])

        row3 = Row3(root)
        row3.btDelete.click()

        self.assertEqual(len(root.kol.objectList), 1)
        self.assertIs(root.kol.objectList[0], second)
        self.assertEqual(root.reviewIndex, 0)


if __name__ == "__main__":
    unittest.main()
