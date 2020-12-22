#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

import unittest

import merge_conf

class BasicTest(unittest.TestCase):
    def test_same_instance(self):
        conf = object()
        config = merge_conf.MultiConfigurationSource(conf)
        conf2 = config.read_configuration()

        self.assertEqual(conf, conf2)

    def test_new_instance(self):
        config = merge_conf.MultiConfigurationSource()
        conf = config.read_configuration()

        self.assertIsNotNone(conf)

    def test_new_instance_correct_type(self):
        config = merge_conf.MultiConfigurationSource()
        conf = config.read_configuration()

        self.assertTrue(isinstance(conf, merge_conf.Namespace))

if __name__ == '__main__':
    unittest.main()
