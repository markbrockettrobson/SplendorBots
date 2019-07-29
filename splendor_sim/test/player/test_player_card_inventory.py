import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.player.player_card_inventory as player_card_inventory
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas


class TestPlayerCardInventory(unittest.TestCase):

    def setUp(self):
        self._max_reserved_cards = 3
        self._mock_card_list = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(30)]
        self._mock_card_set = set(self._mock_card_list)
        self._mock_discount = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        self._mock_cost = {mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 1 for _ in range(3)}
        for index, mock_card in enumerate(self._mock_card_list):
            mock_card.get_victory_points.return_value = 1
            mock_card.get_discount.return_value = self._mock_discount
            mock_card.get_cost.return_value = self._mock_cost
            mock_card.get_name.return_value = "%d" % index

    def test_player_card_inventory_init_valid(self):
        # Arrange
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)
        self.assertEqual(test_player_card_inventory.get_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_init_valid_reserved_cards(self):
        # Arrange
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            {self._mock_card_list[0]},
            set()
        )
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)
        self.assertEqual(test_player_card_inventory.get_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), {self._mock_card_list[0]})
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 1)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_init_valid_cards(self):
        # Arrange
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            {self._mock_card_list[0]}
        )
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {self._mock_discount: 1})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 1)
        self.assertEqual(test_player_card_inventory.get_card_set(), {self._mock_card_list[0]})
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_init_invalid_to_many_reserved_cards(self):
        # Arrange
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_card_inventory.PlayerCardInventory(
                self._max_reserved_cards,
                set(self._mock_card_list[:4]),
                set()
            )

    def test_player_card_inventory_init_invalid_max_reserved_cards(self):
        # Arrange
        self._max_reserved_cards = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_card_inventory.PlayerCardInventory(
                self._max_reserved_cards,
                set(),
                set()
            )

    def test_player_card_inventory_init_valid_max_reserved_cards_zero(self):
        # Arrange
        self._max_reserved_cards = 0
        # Act
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)
        self.assertEqual(test_player_card_inventory.get_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), set())
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)
        self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_get_max_number_of_reserved_cards(self):
        # Arrange
        for i in range(4):
            self._max_reserved_cards = i
            test_player_card_inventory = player_card_inventory.PlayerCardInventory(
                self._max_reserved_cards,
                set(),
                set()
            )
            # Act
            # Assert
            self.assertEqual(test_player_card_inventory.get_max_number_of_reserved_cards(), self._max_reserved_cards)

    def test_player_card_inventory_add_card_valid(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        test_player_card_inventory.add_card(self._mock_card_list[0])
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), {self._mock_discount: 1})
        self.assertEqual(test_player_card_inventory.get_victory_points(), 1)
        self.assertEqual(test_player_card_inventory.get_card_set(), {self._mock_card_list[0]})

    def test_player_card_inventory_add_card_card_already_in_set(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        test_player_card_inventory.add_card(self._mock_card_list[0])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card(self._mock_card_list[0])

    def test_player_card_inventory_add_card_to_reserved(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])
        # Assert
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), {self._mock_card_list[0]})
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 1)

    def test_player_card_inventory_add_card_to_reserved_card_already_in_set(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[0])

    def test_player_card_inventory_add_card_to_reserved_already_full(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        for i in range(self._max_reserved_cards):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[-1])

    def test_player_card_inventory_get_total_discount(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        for i in range(4):
            test_player_card_inventory.add_card(self._mock_card_list[i])
            discount = test_player_card_inventory.get_total_discount()
            # Assert
            self.assertEqual(discount, {self._mock_discount: i + 1})

    def test_player_card_inventory_get_total_discount_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        test_player_card_inventory.add_card(self._mock_card_list[0])
        discount = test_player_card_inventory.get_total_discount()
        premutaion = copy.copy(discount)
        # Act
        discount.pop(list(discount.keys())[0])
        # Assert
        self.assertEqual(test_player_card_inventory.get_total_discount(), premutaion)

    def test_player_card_inventory_get_victory_points(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        for i in range(4):
            test_player_card_inventory.add_card(self._mock_card_list[i])
            # Assert
            self.assertEqual(test_player_card_inventory.get_victory_points(), i + 1)

    def test_player_card_inventory_get_victory_points_reserved_cards_do_not_count(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        for i in range(self._max_reserved_cards):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Assert
        self.assertEqual(test_player_card_inventory.get_victory_points(), 0)

    def test_player_card_inventory_get_card_list(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        for card in self._mock_card_list:
            test_player_card_inventory.add_card(card)
        # Assert
        self.assertEqual(test_player_card_inventory.get_card_set(), self._mock_card_set)

    def test_player_card_inventory_get_card_list_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for card in self._mock_card_list:
            test_player_card_inventory.add_card(card)
        card_set = test_player_card_inventory.get_card_set()
        pre_mutation = copy.copy(card_set)
        # Act
        card_set.pop()
        # Assert
        self.assertEqual(test_player_card_inventory.get_card_set(), pre_mutation)

    def test_player_card_inventory_get_reserved_card_list(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Act
        # Assert
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), set(self._mock_card_list[:3]))

    def test_player_card_inventory_get_reserved_card_list_immutability(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        card_set = test_player_card_inventory.get_reserved_card_set()
        pre_mutation = copy.copy(card_set)
        # Act
        card_set.pop()
        # Assert
        self.assertEqual(test_player_card_inventory.get_reserved_card_set(), pre_mutation)

    def test_player_card_inventory_get_number_of_reserved_cards(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for i in range(3):
            # Act
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
            # Assert
            self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), i + 1)

    def test_player_card_inventory_remove_from_reserved_card_list(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        for card in test_player_card_inventory.get_reserved_card_set():
            # Act
            test_player_card_inventory.remove_from_reserved_card_set(card)
        # Assert
        self.assertEqual(test_player_card_inventory.get_number_of_reserved_cards(), 0)

    def test_player_card_inventory_remove_from_reserved_card_list_card_not_in_reserve(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        for i in range(3):
            test_player_card_inventory.add_card_to_reserved(self._mock_card_list[i])
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_player_card_inventory.remove_from_reserved_card_set(self._mock_card_list[-1])

    def test_player_card_inventory_to_json(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(),
            set()
        )
        # Act
        # Assert
        self.assertEqual(
            {
                "max_reserved_cards": self._max_reserved_cards,
                "reserved_cards": [],
                "cards": []
            },
            test_player_card_inventory.to_json()
        )

    def test_player_card_inventory_to_json_non_full(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(self._mock_card_list[:1]),
            set(self._mock_card_list[-1:])
        )
        # Act
        # Assert
        self.assertEqual(
            {
                "max_reserved_cards": self._max_reserved_cards,
                "reserved_cards": [card.get_name() for card in set(self._mock_card_list[:1])],
                "cards": [card.get_name() for card in set(self._mock_card_list[-1:])]
            },
            test_player_card_inventory.to_json()
        )

    def test_player_card_inventory_to_json_complies_with_schema(self):
        # Arrange
        test_player_card_inventory = player_card_inventory.PlayerCardInventory(
            self._max_reserved_cards,
            set(self._mock_card_list[:2]),
            set(self._mock_card_list[2:])
        )
        test_json_validator = json_validator.JsonValidator(json_schemas.JSON_PLAYER_CARD_INVENTORY)
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_player_card_inventory.to_json())
        )
