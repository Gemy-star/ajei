#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add new translations for branches section
"""

import re

# New translations to add
new_translations = {
    "الفروع": "الفروع",
    "العلامات التجارية": "العلامات التجارية",
}

def add_translations(po_file_path, lang_translations):
    """Add translations to .po file"""
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for msgid, msgstr in lang_translations.items():
        # Check if translation already exists
        if f'msgid "{msgid}"' in content:
            # Update empty msgstr
            pattern = f'msgid "{re.escape(msgid)}"\\nmsgstr ""'
            replacement = f'msgid "{msgid}"\\nmsgstr "{msgstr}"'
            content = re.sub(pattern, replacement, content)

    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {po_file_path}")

# Arabic translations
ar_translations = {
    "الفروع": "الفروع",
    "العلامات التجارية": "العلامات التجارية",
}

# English translations
en_translations = {
    "الفروع": "Branches",
    "العلامات التجارية": "Our Brands",
}

# Update files
add_translations(r'c:\WORK\SELF\ajei_project\locale\ar\LC_MESSAGES\django.po', ar_translations)
add_translations(r'c:\WORK\SELF\ajei_project\locale\en\LC_MESSAGES\django.po', en_translations)

print("\\n✅ Translations added!")
print("Run: python manage.py compilemessages")
