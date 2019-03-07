import copy
import typing
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.player.player_card_inventory as player_card_inventory


class TestPlayerCardInventory(unittest.TestCase):

    def setUp(self):
        self._max_reserved_cards = 3
        self._mock_card_list = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(30)]
        self._mock_discount = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(2)]
        self._mock_cost = {mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 1 for _ in range(3)}
        for i, _mock_card in enumerate(self._mock_card_list):
            _mock_card.get_victory_points.return_value = 1
            _mock_card.get_discount.return_value = self._mock_discount[(i + 1) % 1]
            _mock_card.get_cost.return_value = self._mock_cost

    def test_player_card_inventory_init_valid(self):
        # Arrange
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)
        self.assertEqual(test_player_card_inventory.get_card_list(), [])
        self.assertEqual(test_player_card_inventory.get_reserved_card_list(), [])
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_init_invalid_max_reserved_cards(self):
        # Arrange
        self._max_reserved_cards = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)

    def test_player_card_inventory_init_valid_max_reserved_cards_zero(self):
        # Arrange
        self._max_reserved_cards = 0
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)
        self.assertEqual(test_player_card_inventory.get_card_list(), [])
        self.assertEqual(test_player_card_inventory.get_reserved_card_list(), [])
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_get_max_number_of_reserved_cards(self):
        # Arrange
        for i in range(4):
            self._max_reserved_cards = i
            test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
            # Act
            # Assert
            self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_add_card_valid(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        test_player_card_inventory.add_card(self._mock_card_list[0])
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), self._mock_discount)
        self.assertEqual(test_player_card_inventory.get_victory_points(), 1)
        self.assertEqual(test_player_card_inventory.get_card_list(), [self._mock_card_list[0]])

    def test_player_card_inventory_add_card_card_already_in_set(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        test_player_card_inventory.add_card(self._mock_card_list[0])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card(self._mock_card_list[0])

    def test_player_card_inventory_add_card_to_reserved(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])
        # Assert
        self.assertEqual(test_player_card_inventory.add_card_to_reserved(), [self._mock_card_list[0]])
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 1)

    def test_player_card_inventory_add_card_to_reserved_card_already_in_set(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])

    def test_player_card_inventory_add_card_to_reserved_already_full(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        for i in range(self._max_reserved_cards):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[-1])

    def test_player_card_inventory_get_total_discount(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        for i in range(4):
            test_player_card_inventory.add_card(self._mock_card_list[i])
            discount = test_player_card_inventory.get_total_discount()
            # Assert
            for coin in self._mock_discount:
                self.assertEqual(discount[coin], i + 1)

    def test_player_card_inventory_get_total_discount_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        test_player_card_inventory.add_card(self._mock_card_list[0])
        discount = test_player_card_inventory.get_total_discount()
        premutaion = copy.copy(discount)
        # Act
        discount.pop(list(discount.keys())[0])
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), premutaion)

    def test_player_card_inventory_get_victory_points(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        for i in range(4):
            test_player_card_inventory.add_card(self._mock_card_list[i])
            # Assert
            self.assertEqual(test_player_card_inventory.get_victory_points(), i + 1)

    def test_player_card_inventory_get_victory_points_reserved_cards_do_not_count(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        for i in range(self._max_reserved_cards):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Assert
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)

    def test_player_card_inventory_get_card_list(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        # Act
        for card in self._mock_card_list:
            test_player_card_inventory.add_card(card)
        # Assert
        self.assertEqual(test_player_card_inventory.get_card_list(), self._mock_card_list[0])

    def test_player_card_inventory_get_card_list_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        for card in self._mock_card_list:
            test_player_card_inventory.add_card(card)
        card_list = test_player_card_inventory.get_card_list()
        pre_mutation = copy.copy(card_list)
        # Act
        card_list.pop()
        # Assert
        self.assertEqual(test_player_card_inventory.get_card_list(), pre_mutation)

    def test_player_card_inventory_get_reserved_card_list(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Act
        # Assert
        self.assertEqual(test_player_card_inventory.get_reserved_card_list(), self._mock_card_list[:3])

    def test_player_card_inventory_get_reserved_card_list_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        card_list = test_player_card_inventory.get_reserved_card_list()
        pre_mutation = copy.copy(card_list)
        # Act
        card_list.pop()
        # Assert
        self.assertEqual(test_player_card_inventory.get_reserved_card_list(), pre_mutation)

    def test_player_card_inventory_get_number_of_reserved_cards(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(self._max_reserved_cards)
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
            # Assert
            self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), i + 1)
