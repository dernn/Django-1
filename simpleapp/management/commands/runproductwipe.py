from django.core.management import BaseCommand, CommandError

from simpleapp.models import Product


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <команда> --help"
    help = 'Delete all products'

    # Напоминание о миграциях.
    # Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    requires_migrations_checks = True

    def handle(self, *args, **options):
        # здесь код, который выполняется при вызове команды
        self.stdout.readable()
        # спрашиваем пользователя, действительно ли он хочет удалить все товары
        self.stdout.write(
            'Do you really want to delete all products? [yes/no]')
        answer = input()  # считываем подтверждение

        # в случае подтверждения удаляем все товары
        if answer == 'yes':
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Succesfully products removed!'))
            return

        # в случае неправильного подтверждения, говорим, что в доступе отказано
        self.stdout.write(
            self.style.ERROR('Access denied'))
