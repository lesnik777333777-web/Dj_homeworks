import csv
from django.core.management.base import BaseCommand
from phones.models import Phone

class Command(BaseCommand):
    help = 'Импорт данных о телефонах из CSV файла'

    def handle(self, *args, **options):
        file_path = 'phones.csv'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    Phone.objects.create(
                        id=int(row['id']),
                        name=row['name'],
                        price=int(row['price']),
                        image=row['image'],
                        release_date=row['release_date'],
                        lte_exists=row['lte_exists'] == 'True'
                    )
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены в базу данных'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден.'))
