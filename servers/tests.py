from django.test import TestCase

class SimpleTest(TestCase):
    def test_basice_addition(self):

        self.assertEqual(1+1,2)