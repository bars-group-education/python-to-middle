from abc import ABCMeta, abstractmethod
from collections import defaultdict
from enum import IntEnum


class Language(IntEnum):
    RUSSIAN = 1
    ENGLISH = 2
    GERMAN = 3


class Mediator(metaclass=ABCMeta):
    """ Абстрактный класс медиатора - переводчика """

    @abstractmethod
    def translate(self, word: str, language_from: Language) -> str:
        """
            Переводит слово с одного языка на другой
        :param word: слово для перевода
        :param language_from: с какого языка переводим
        :return: переведенное слово
        """
        pass


class Foreigner:
    """Класс иностранца"""

    def __init__(self, language: Language, mediator: Mediator):
        """
            Инициализация класса
        :param language: язык иностранца
        """
        self.language = language
        self.mediator = mediator
        self._listen_word = ''

    @property
    def last_listen_word(self) -> str:
        """
            Получаем последнее услышанное слово
        :return: услышанное слово
        """
        return self._listen_word

    @last_listen_word.setter
    def last_listen_word(self, word: str):
        """
            Устанавливаем последнее услышанное слово
        :param word: услышанное слово
        """
        self._listen_word = word

    def say(self, word: str):
        """
            Иностранец произносит слово на своем языке
        :param word: произнесенное слово
        """
        self.mediator.translate(word, self.language)


class Translator(Mediator):
    """Переводчик с одного языка на другой"""

    def __init__(self):
        super().__init__()
        self.foreigners = {}

    def add_foreigner(self, language: Language, foreigner: Foreigner):
        """
            Добавляет иностранца, для которого нужно переводить
        :param language: язык иностранца
        :param foreigner: иностранец
        """
        self.foreigners[language] = foreigner

    def translate(self, word: str, language_from: Language) -> str:
        # нужно добавить свой код сюда
        all_words = dictionary.get_all_words_by_specific_word(word, language_from)

        for language_to, foreigner in self.foreigners.items():
            foreigner.last_listen_word = all_words[language_to]

        return word


class UniWords(IntEnum):
    CAT = 1
    DOG = 2


class Dictionary:

    def __init__(self) -> None:
        super().__init__()
        self._specific_to_uni = defaultdict(int)
        self._uni_to_specific = defaultdict(dict)

    def add_word(self, specific_word, language, uni_word):
        self._specific_to_uni[(specific_word, language)] = uni_word
        self._uni_to_specific[uni_word][language] = specific_word

    def get_all_words_by_specific_word(self, specific_word, language):
        uni_word = self._specific_to_uni[(specific_word, language)]
        all_words = self._uni_to_specific[uni_word]

        return all_words


dictionary = Dictionary()

dictionary.add_word('cat', Language.ENGLISH, UniWords.CAT)
dictionary.add_word('кот', Language.RUSSIAN, UniWords.CAT)
dictionary.add_word('katze', Language.GERMAN, UniWords.CAT)

dictionary.add_word('dog', Language.ENGLISH, UniWords.DOG)
dictionary.add_word('собака', Language.RUSSIAN, UniWords.DOG)
dictionary.add_word('hund', Language.GERMAN, UniWords.DOG)

