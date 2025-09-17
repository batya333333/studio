from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userprofile.models import Profile


class Command(BaseCommand):
    help = 'Заполняет пустые поля Profile из связанных полей User (first_name, last_name, email)'

    def handle(self, *args, **options):
        updated_count = 0
        created_count = 0

        for user in User.objects.all().iterator():
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1

            modified = False
            if user.first_name and not profile.first_name:
                profile.first_name = user.first_name
                modified = True
            if user.last_name and not profile.last_name:
                profile.last_name = user.last_name
                modified = True
            if user.email and not profile.email:
                profile.email = user.email
                modified = True

            if modified:
                profile.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово. Обновлено профилей: {updated_count}, создано профилей: {created_count}'
        ))


