# speed_test

Скрипт измеряет скорость скачивания в `MB/s`:
- делает 10 последовательных запросов к URL (по умолчанию),
- считает общее время и объем,
- печатает только итоговую скорость.

## Требования

- Python 3.9+

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python speed_test.py "<URL>"
```

Пример:

```bash
python speed_test.py "https://speed.cloudflare.com/__down?bytes=5000000"
```

## Параметры

- `url` — адрес файла (обязательный)
- `requests_count` — количество запросов (необязательный, по умолчанию `10`)
- `--timeout` — таймаут одного запроса в секундах (по умолчанию `30`)

Пример с параметрами:

```bash
python speed_test.py "https://speed.cloudflare.com/__down?bytes=5000000" 10 --timeout 30
```