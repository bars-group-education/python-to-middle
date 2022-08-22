from datetime import date

from django.test import (
    TestCase,
)

from block_9.indexes.task_1.implementation import (
    filter_by_fio,
    filter_works_by_period,
    filter_by_country,
    filter_by_word_in_additional_info,
)


class MyTestCase(TestCase):
    def _test_seq_scan(self, query):
        self.assertFalse('Seq Scan' in query.explain())

    def test_filter_by_fio(self):
        query = filter_by_fio('Иванов Иван Иванович')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 0)

        query = filter_by_fio('Овчинникова Ольга Сергеевна')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 1)

        query = filter_by_fio('Паркер Джон Адамс Старший')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 0)

    def test_filter_works_by_period(self):
        query = filter_works_by_period(date(2022, 1, 1), date(2022, 12, 31))
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 10000)

        query = filter_works_by_period(date(2062, 1, 1), date(2062, 12, 31))
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 193)

        query = filter_works_by_period(date(2070, 1, 1), date(2070, 12, 31))
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 0)

    def test_filter_by_country(self):
        query = filter_by_country('LR')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 47)

        query = filter_by_country('NA')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 55)

        query = filter_by_country('ZZ')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 0)

    def test_filter_by_word_in_additional_info(self):
        query = filter_by_word_in_additional_info('Оператор')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 117)

        query = filter_by_word_in_additional_info('Пульмонолог')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 15)

        query = filter_by_word_in_additional_info('Винодел')
        self._test_seq_scan(query)
        self.assertEqual(query.count(), 0)
