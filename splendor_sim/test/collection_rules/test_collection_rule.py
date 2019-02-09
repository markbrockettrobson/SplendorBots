import unittest

from splendor_sim.collection_rules.collection_rule import CollectionRule


class TestCollectionRule(unittest.TestCase):

    def setUp(self):
        self._collection_rule = CollectionRule()

    def test_collection_rule_str(self):
        # ASSEMBLE
        expected = "CollectionRule super class"

        # ACT
        real = str(self._collection_rule)

        # ASSERT
        assert expected == real

    def test_collection_rule_get_description(self):
        # ASSEMBLE
        expected = "CollectionRule super class"

        # ACT
        real = self._collection_rule.get_description()

        # ASSERT
        assert expected == real

    def test_collection_rule_is_valid(self):
        # ASSEMBLE
        expected = False

        # ACT
        real = self._collection_rule.is_valid(None, None)

        # ASSERT
        assert expected == real
