from abc import abstractmethod, ABCMeta
from enum import IntEnum, Enum


class Language(IntEnum):
    RUSSIAN = 1
    ENGLISH = 2
    GERMAN = 3
    FRANCE = 4


DictionaryTranslator = {
    Language.RUSSIAN: {
        'кот': {
            Language.ENGLISH: 'cat',
            Language.GERMAN: 'katze'
        },
        'собака': {
            Language.ENGLISH: 'dog',
            Language.GERMAN: 'hund'
        }
    },
    Language.ENGLISH: {
        'cat': {
            Language.RUSSIAN: 'кот',
            Language.GERMAN: 'katze'
        },
        'dog': {
            Language.RUSSIAN: 'собака',
            Language.GERMAN: 'hund'
        }
    },
    Language.GERMAN: {
        'katze': {
            Language.RUSSIAN: 'кот',
            Language.ENGLISH: 'cat'
        },
        'hund': {
            Language.RUSSIAN: 'собака',
            Language.ENGLISH: 'dog'
        }
    }
}


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

    def translate(self, word: str, language_from: Language):
        language_dictionary = DictionaryTranslator.get(language_from)

        if not language_dictionary:
            raise KeyError(f'Словарь {language_from.name} отсутствует')

        for foreigner in self.foreigners.values():
            if foreigner.language == language_from:
                foreigner.last_listen_word = word
            else:
                foreigner.last_listen_word = language_dictionary.get(word).get(foreigner.language)