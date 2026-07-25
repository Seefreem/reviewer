import json
import tempfile
import unittest
from pathlib import Path

from src.vocabularyFile import (
    create_vocabulary,
    load_vocabulary,
    metadata_path,
)


class VocabularyFileTests(unittest.TestCase):
    def test_create_empty_vocabulary_with_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            vocabulary_path = Path(directory) / "ielts.json"

            created_path, metadata = create_vocabulary(
                vocabulary_path,
                {
                    "title": "IELTS",
                    "description": "Listening words",
                    "sourceLanguage": "English",
                    "targetLanguage": "Chinese",
                    "tags": "ielts; listening; ",
                },
            )

            self.assertEqual(Path(created_path), vocabulary_path.resolve())
            self.assertEqual(json.loads(vocabulary_path.read_text(encoding="utf-8")), [])
            self.assertTrue(metadata_path(vocabulary_path).exists())
            self.assertEqual(metadata["tags"], ["ielts", "listening"])

            objects, loaded_metadata = load_vocabulary(vocabulary_path)
            self.assertEqual(objects, [])
            self.assertEqual(loaded_metadata["title"], "IELTS")
            self.assertEqual(loaded_metadata["description"], "Listening words")
            self.assertIn("createdAt", loaded_metadata)

    def test_existing_list_file_works_without_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            vocabulary_path = Path(directory) / "legacy.json"
            vocabulary_path.write_text('[{"context": "word"}]', encoding="utf-8")

            objects, metadata = load_vocabulary(vocabulary_path)

            self.assertEqual(objects, [{"context": "word"}])
            self.assertEqual(metadata["title"], "legacy")

    def test_rejects_non_list_vocabulary(self):
        with tempfile.TemporaryDirectory() as directory:
            vocabulary_path = Path(directory) / "invalid.json"
            vocabulary_path.write_text('{"context": "word"}', encoding="utf-8")

            with self.assertRaises(ValueError):
                load_vocabulary(vocabulary_path)


if __name__ == "__main__":
    unittest.main()
