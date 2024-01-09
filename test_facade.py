import unittest
import os
from unittest.mock import patch, mock_open, call
from facade import GameFacade, Level

class MockLevel:
    def __init__(self, filename):
        self.filename = filename

class TestGameFacade(unittest.TestCase):
    def setUp(self):
        self.game = GameFacade()

    @patch('builtins.open', new_callable=mock_open, read_data="player1,100,level1\nplayer2,200,level2\n")
    def test_load_high_scores(self):
        self.game.load_high_scores("any_file_path")
        self.assertEqual(self.game.get_high_scores(), [('player1', 100, 'level1'), ('player2', 200, 'level2')])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_high_scores(self, mock_file):
        self.game.level = MockLevel('test_level.txt')
        self.game.save_high_score('test_player', 150)
        mock_file.assert_called_once_with('high_scores.txt', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('test_player,150, test_level\n')

    @patch('facade.os.listdir')  # заменяем функцию os.listdir на мок
    @patch('facade.Level')  # заменяем класс Level на мок
    def test_load_levels(self, mock_level, mock_listdir):
        # Настраиваем моки
        mock_listdir.return_value = ['level1.txt', 'level2.txt',
                                     'not_a_level.pdf']  # os.listdir теперь вернет этот список файлов

        game = GameFacade()  # создаем экземпляр класса, который будем тестировать

        # Вызываем тестируемый метод
        game.load_levels('levels')  # вызываем метод с аргументом 'levels'

        # создаем список ожидаемых вызовов функции Level с правильными аргументами
        calls = [call(os.path.join('levels', 'level1.txt')), call(os.path.join('levels', 'level2.txt'))]
        mock_level.assert_has_calls(calls,
                                    any_order=True)  # проверяем, что функция Level была вызвана с правильными аргументами
        self.assertEqual(2, len(game.levels))  # проверяем, что в game.levels теперь два элемента

if __name__ == '__main__':
    unittest.main()