#!/usr/bin/env bash
# خروج فوری اگر دستوری با وضعیت غیر صفر خارج شود.
set -e

echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Running collectstatic ---"
# اجرای collectstatic با کلاس ذخیره‌سازی سفارشی
python manage.py collectstatic --noinput

echo "--- Running database migrations ---"
# اعمال Migration ها
python manage.py migrate

echo "--- Build successful ---"
