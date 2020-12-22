#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of multiconf-py
# (see https://github.com/carstencodes/multiconf-py).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

import unittest

import multiconf

class BasicTest(unittest.TestCase):
    def test_same_instance(self):
        conf = object()
        config = multiconf.MultiConfigurationSource(conf)
        conf2 = config.read_configuration()

        self.assertEqual(conf, conf2)

    def test_new_instance(self):
        config = multiconf.MultiConfigurationSource()
        conf = config.read_configuration()

        self.assertIsNotNone(conf)

    def test_new_instance_correct_type(self):
        config = multiconf.MultiConfigurationSource()
        conf = config.read_configuration()

        self.assertTrue(isinstance(conf, multiconf.Namespace))

if __name__ == '__main__':
    unittest.main()
