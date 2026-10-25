import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from phones.models import Phone

class Command(BaseCommand):
    help = 'Импортирует данные о телефонах из CSV файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')

                for row in reader:
                    phone_id = int(row['id'])
                    name = row['name'].strip()
                    price = int(row['price'])
                    image = row['image'].strip()
                    release_date = row['release_date'].strip()
                    lte_exists = row['lte_exists'].strip().lower() == 'true'

                    Phone.objects.update_or_create(
                        id=phone_id,
                        defaults={
                            'name': name,
                            'price': price,
                            'image': image,
                            'release_date': release_date,
                            'lte_exists': lte_exists,
                            'slug': slugify(name)
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))