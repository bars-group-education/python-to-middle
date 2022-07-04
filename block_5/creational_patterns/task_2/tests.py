import unittest

from block_5.creational_patterns.task_2.implementation import ZooOwner, CatBuilder, CuckooBuilder, FishBuilder


class MyTestCase(unittest.TestCase):

    def test_cat_create(self):
        zoo_owner = ZooOwner()
        cat_builder = CatBuilder()
        zoo_owner.create_animal(cat_builder)
        cat = cat_builder.animal

        self.assertEqual(cat.name, 'cat')
        self.assertEqual(cat.legs_count, 4)
        self.assertEqual(cat.wing_exist, False)
        self.assertEqual(cat.roar, 'meow')

    def test_cockoo_create(self):
        zoo_owner = ZooOwner()
        cuckoo_builder = CuckooBuilder()
        zoo_owner.create_animal(cuckoo_builder)
        cuckoo = cuckoo_builder.animal

        self.assertEqual(cuckoo.name, 'cuckoo')
        self.assertEqual(cuckoo.legs_count, 2)
        self.assertEqual(cuckoo.wing_exist, True)
        self.assertEqual(cuckoo.roar, 'cucu')

    def test_fist_create(self):
        zoo_owner = ZooOwner()
        fish_builder = FishBuilder()
        zoo_owner.create_animal(fish_builder)
        fish = fish_builder.animal

        self.assertEqual(fish.name, 'fish')
        self.assertEqual(fish.legs_count, 0)
        self.assertEqual(fish.wing_exist, False)
        self.assertEqual(fish.roar, None)





