"""
Этап 1: Минимальный прототип с конфигурацией.
Требования:
- Настройка через CLI: --package, --repo, --test-mode, --version, --output-format, --max-depth
- Вывод всех параметров в формате "ключ: значение"
- Обработка ошибок (отсутствие обязательных параметров, неверные значения)
- Никаких внешних зависимостей (только стандартная библиотека)
"""

import sys

def trim(s):
    """Удаляет пробелы и табы в начале и конце строки."""
    return s.strip()

def is_url(s):
    """Проверяет, похожа ли строка на URL."""
    return s.startswith(('http://', 'https://'))

def parse_args(argv):
    """Ручной парсинг аргументов (без argparse для прозрачности)."""
    config = {
        'package': None,
        'repo': None,
        'test_mode': False,
        'version': '1.0',
        'output_format': 'ascii-tree',
        'max_depth': 5
    }

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ('--package', '-p'):
            if i + 1 >= len(argv):
                raise ValueError("Опция --package требует значения.")
            config['package'] = trim(argv[i + 1])
            i += 2
        elif arg in ('--repo', '-r'):
            if i + 1 >= len(argv):
                raise ValueError("Опция --repo требует значения.")
            config['repo'] = trim(argv[i + 1])
            i += 2
        elif arg in ('--test-mode', '-t'):
            config['test_mode'] = True
            i += 1
        elif arg in ('--version', '-v'):
            if i + 1 >= len(argv):
                raise ValueError("Опция --version требует значения.")
            config['version'] = trim(argv[i + 1])
            i += 2
        elif arg in ('--output-format', '-o'):
            if i + 1 >= len(argv):
                raise ValueError("Опция --output-format требует значения.")
            fmt = trim(argv[i + 1])
            if fmt not in ('ascii-tree', 'json', 'dot'):
                raise ValueError("Неподдерживаемый формат вывода. Допустимые: ascii-tree, json, dot.")
            config['output_format'] = fmt
            i += 2
        elif arg in ('--max-depth', '-d'):
            if i + 1 >= len(argv):
                raise ValueError("Опция --max-depth требует значения.")
            try:
                depth = int(trim(argv[i + 1]))
                if depth < 0:
                    raise ValueError("Максимальная глубина не может быть отрицательной.")
                config['max_depth'] = depth
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError("Неверное значение для --max-depth. Ожидается целое число.")
                else:
                    raise
            i += 2
        else:
            raise ValueError(f"Неизвестная опция: {arg}")

    return config
def validate_config(config):
        """Проверяет корректность параметров."""
        if not config['package']:
            raise ValueError("Имя анализируемого пакета (--package) обязательно.")

        if not config['repo']:
            raise ValueError("URL или путь к репозиторию (--repo) обязателен.")

        if config['test_mode'] and is_url(config['repo']):
            raise ValueError("В режиме --test-mode репозиторий должен быть локальным путём (не URL).")

def display_config(config):
        """Выводит все параметры в формате ключ: значение (только для Этапа 1)."""
        print(" Конфигурация ")
        for key, value in config.items():
            print(f"{key}: {value}")

def main():
        print(" Запуск инструмента визуализации графа зависимостей (Этап 1)")
        try:
            config = parse_args(sys.argv)
            validate_config(config)
            display_config(config)
            print("\n Этап 1 успешно завершён. Приложение настроено.")
        except Exception as e:
            print(f" Ошибка: {e}", file=sys.stderr)
            sys.exit(1)
if __name__ == "__main__":
    main()