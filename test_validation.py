import unittest

from validation import validate_text


class TestValidation(unittest.TestCase):
    def test_valid_text(self):
        self.assertIsNone(validate_text("I went to class this morning."))

    def test_punctuation(self):
        self.assertIsNotNone(validate_text("!!!!!!!!"))

    def test_emoji_only(self):
        self.assertIsNotNone(validate_text("😂😂😂😂"))

    def test_control_characters(self):
        self.assertIsNotNone(validate_text("Hello\x00world"))

    def test_multiline(self):
        self.assertIsNone(validate_text("Hello.\nHow are you?"))

    def test_valid_text_with_emoji(self):
        self.assertIsNone(validate_text("I had a great day! 😂"))

    def test_unicode_letters(self):
        self.assertIsNone(validate_text("Bonjour, ça va?"))

    def test_repetitive_characters(self):
        self.assertEqual(
            validate_text("a" * 200),
            "repetitive_text",
        )

    def test_repetitive_words(self):
        self.assertEqual(
            validate_text("hello " * 80),
            "repetitive_text",
        )

    def test_normal_repetition(self):
        self.assertIsNone(validate_text("I was very, very excited today."))


if __name__ == "__main__":
    unittest.main()
