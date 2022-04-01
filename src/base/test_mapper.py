from typing import List, Tuple
from unittest import TestCase
from src.base.mapper import TwoWayDict


class TestToWayDict(TestCase):
    def test_mapper_with_str(self):
        mapped_entities_list = [
            ("User", "DbUser"),
            ("Role", "DbRole")
        ]

        self._common_test_logic(mapped_entities_list=mapped_entities_list)

    def test_mapper_with_type(self):
        mapped_entities_list = [
            (type("User", (object, ), {}), type("DbUser", (object, ), {})),
            (type("Role", (object, ), {}), type("DbRole", (object, ), {}))
        ]
        
        self._common_test_logic(mapped_entities_list=mapped_entities_list)

    def _common_test_logic(self, mapped_entities_list: List[Tuple]):
        two_way_dict = TwoWayDict(mapped_entities_list)

        for it in mapped_entities_list:
            self.assertTrue(it[0] in two_way_dict)
            self.assertTrue(it[1] in two_way_dict)
            self.assertEqual(two_way_dict[it[0]], it[1])
            self.assertEqual(two_way_dict[it[1]], it[0])
