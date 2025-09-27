from django.core.management.base import BaseCommand
import shutil
from pathlib import Path

class Command(BaseCommand):
    help = 'Create a .env file from .env.example if it does not exist'

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parents[4]
        src = base / '.env.example'
        dst = base / '.env'
        if dst.exists():
            self.stdout.write(self.style.NOTICE('.env already exists'))
            return
        if not src.exists():
            self.stdout.write(self.style.ERROR('.env.example not found'))
            return
        shutil.copy(src, dst)
        self.stdout.write(self.style.SUCCESS('Created .env from .env.example'))
