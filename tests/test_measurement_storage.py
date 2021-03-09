from unittest import TestCase
import pandas as pd
import src.measurement_storage


class TestCaching(TestCase):
    def setUp(self) -> None:
        self.filepath = 'some/file/path/'
        self.filename = 'testfilename'

    def test__save_json(self):