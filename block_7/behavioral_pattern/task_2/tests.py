import unittest

from block_7.behavioral_pattern.task_2.implementation import Translator, Foreigner, Language


class MyTestCase(unittest.TestCase):

    def test_german_say(self):
        translator = Translator()
        russian_man = Foreigner(Language.RUSSIAN, translator)
        english_man = Foreigner(Language.ENGLISH, translator)
        german_man = Foreigner(Language.GERMAN, translator)
        translator.add_foreigner(Language.RUSSIAN, russian_man)
        translator.add_foreigner(Language.ENGLISH, english_man)
        translator.add_foreigner(Language.GERMAN, german_man)

        german_man.say('katze')
        self.assertEqual(english_man.last_listen_word, 'cat')
        self.assertEqual(russian_man.last_listen_word, 'кот')
        self.assertEqual(german_man.last_listen_word, 'katze')

    def test_english_say(self):
        translator = Translator()
        russian_man = Foreigner(Language.RUSSIAN, translator)
        english_man = Foreigner(Language.ENGLISH, translator)
        german_man = Foreigner(Language.GERMAN, translator)
        translator.add_foreigner(Language.RUSSIAN, russian_man)
        translator.add_foreigner(Language.ENGLISH, english_man)
        translator.add_foreigner(Language.GERMAN, german_man)

        english_man.say('dog')
        self.assertEqual(english_man.last_listen_word, 'dog')
        self.assertEqual(russian_man.last_listen_word, 'собака')
        self.assertEqual(german_man.last_listen_word, 'hund')
