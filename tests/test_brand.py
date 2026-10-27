# SPDX-License-Identifier: GPL-3.0-or-later
import json, hashlib, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Brand(unittest.TestCase):
    def test_search_web_icon_kit_is_unchanged(self):
        kit = ROOT / 'vigiltech/product-icons/search'
        meta = json.loads((kit / 'SOURCE.json').read_text())
        self.assertEqual(meta['product'], 'search')
        for item in meta['files']:
            self.assertEqual(hashlib.sha256((kit / item['path']).read_bytes()).hexdigest(), item['sha256'], item['path'])

    def test_design_system_files_match_manifest(self):
        root = ROOT / 'vigiltech'
        for name, digest in json.loads((root / 'UPSTREAM.json').read_text())['sha256'].items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest, name)

    def test_theme_uses_new_namespace_and_safe_button_pink(self):
        css = (ROOT / 'vigiltech-search.css').read_text()
        for old in ['.altstack-', '.artemis-', '--cs-', '#273941']:
            self.assertNotIn(old, css)
        self.assertIn('var(--vt-pink-600)', css)
        self.assertNotIn('#ff0058', css.lower())

    def test_brand_script_names_and_licence_are_kept(self):
        script = (ROOT / 'brand.py').read_text()
        self.assertIn('Vigil Search', script)
        for old in ['AltStack Search', 'Artemis Softworks']:
            self.assertNotIn(old, script)
        self.assertIn('GNU AFFERO GENERAL PUBLIC LICENSE', (ROOT / 'LICENSE').read_text())
        self.assertIn('AGPL-3.0-or-later', (ROOT / 'Dockerfile').read_text())


if __name__ == '__main__':
    unittest.main()
