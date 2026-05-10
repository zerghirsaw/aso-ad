from django.core.management.base import BaseCommand
import json
import os

class Command(BaseCommand):
    help = 'Tactical CLI for Exoskeleton ASO-AD'
    rules_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'rules.json')

    def add_arguments(self, parser):
        parser.add_argument('--add', type=str, help='Kategori: ACTIONS, TARGETS, BYPASS, SAFE')
        parser.add_argument('--word', type=str, help='Kata kunci yang ingin dimasukkan')
        parser.add_argument('--list', action='store_true', help='Tampilkan semua aturan aktif')

    def handle(self, *args, **options):
        with open(self.rules_path, 'r') as f:
            data = json.load(f)

        if options['list']:
            self.stdout.write(self.style.SUCCESS(f"Current Rules: {json.dumps(data, indent=4)}"))
            return

        category_map = {
            'ACTIONS': 'ACTIONS',
            'TARGETS': 'INTERNAL_TARGETS',
            'BYPASS': 'SYSTEM_BYPASS',
            'SAFE': 'SAFE_CONTEXT'
        }

        cat = options['add']
        word = options['word']

        if cat and word:
            key = category_map.get(cat.upper())
            if key and word not in data[key]:
                data[key].append(word.lower())
                with open(self.rules_path, 'w') as f:
                    json.dump(data, f, indent=4)
                self.stdout.write(self.style.SUCCESS(f"Successfully added '{word}' to {key}"))
            else:
                self.stdout.write(self.style.WARNING("Failed to add or word already exists."))
