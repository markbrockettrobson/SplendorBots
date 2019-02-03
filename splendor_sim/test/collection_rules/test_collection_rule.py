from splendor_sim.collection_rules.collection_rule import CollectionRule


class TestCollectionRule:

    @staticmethod
    def setup():
        collection_rule = CollectionRule()
        return collection_rule

    def test_collection_rule_str(self):
        # ASSEMBLE
        # ACT
        collection_rule = self.setup()
        expected = "CollectionRule super class"

        # ACT
        real = str(collection_rule)

        # ASSERT
        assert expected == real

    def test_collection_rule_get_description(self):
        # ASSEMBLE
        collection_rule = self.setup()
        expected = "CollectionRule super class"

        # ACT
        real = collection_rule.get_description()

        # ASSERT
        assert expected == real

    def test_collection_rule_is_valid(self):
        # ASSEMBLE
        collection_rule = self.setup()
        expected = False

        # ACT
        real = collection_rule.is_valid(None, None)

        # ASSERT
        assert expected == real
