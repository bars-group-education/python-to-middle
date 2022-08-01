from abc import ABC
from abc import abstractmethod
from enum import IntEnum


class Language(IntEnum):
    RUSSIAN = 1
    ENGLISH = 2
    GERMAN = 3


words_cat = {
    Language.ENGLISH: 'cat',
    Language.RUSSIAN: 'кот',
    Language.GERMAN: 'katze',
}

words_dog = {
    Language.ENGLISH: 'dog',
    Language.RUSSIAN: 'собака',
    Language.GERMAN: 'hund',
}
words_list = [words_cat, words_dog]
dictionary = dict()
for words in words_list:
    for word in words.values():
        dictionary.update({word: words})


class Mediator(ABC):
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
        for language in self.foreigners:
            self.foreigners[language].last_listen_word = dictionary[word][
                language
            ]