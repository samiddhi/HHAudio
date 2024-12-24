from .text_processor import ITextProcessor
from aksharamukha import transliterate
import re


class PaliTextProcessor(ITextProcessor):
    def process_text(self, text: str) -> str:

        text = self.process_latin(text)
        text = self.latin_to_kannada(text)
        text = self.process_kannada(text)

        return text

    def process_latin(self, text: str) -> str:
        replacements = {
            "’ti?": "?’ ti?",
            "'ti?": "?' ti?",
            "”ti?": "?” ti.",
            '"ti?': '?" ti.',
            "’ti.": ".’ ti.",
            "'ti.": ".' ti.",
            "”ti.": ".” ti.",
            '"ti.': '." ti.',
            "’ti": "’ ti",
            "'ti": "' ti",
            "”ti": "” ti",
            '"ti': '" ti',
            '”?': '?”',
            '”.': '.”',
            ' ... pe ... ': ', pe, ',

            # Experimental. Some voices weren't pausing here where they really oughta.
            "— ‘": "... ‘",
            "— “": "... “",

            "a,": 'a – ',
            "a.": 'a – .',
            "a?": 'a – ?',
            "a-": 'aa –',
            "a-": 'aa –',
            "a—": 'aa –',
            "a —": 'a –',
            "a:": 'a –:',
            "a;": 'a –;',

            # "'Pagālho?' What language is that even supposed to be? OHH, pagāḷho" -Anīgha (Probably)
            "ḷ": 'l',

            "ññ": 'nny',
            "ña": 'nya',
            "ñā": 'nyā',
            "ñi": 'nyi',
            "ñī": 'nyī',
            "ñu": 'nyu',
            "ñū": 'nyū',
            "ñe": 'nye',
            "ño": 'nyo'
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r'\d+\.?', '', text)
        text = re.sub(r'\s+', ' ', text)

        return text

    def latin_to_kannada(self, text: str) -> str:
        return transliterate.process('IAST', 'Kannada', text)  # Example, adjust as necessary

    def process_kannada(self, text: str) -> str:
        replacements = {
            " — ": "- ",

            # ph's
            "ಫಾ": "ಪ್ಹಾ",
            "ಫಿ": "ಪ್ಹಿ",
            "ಫೀ": "ಪ್ಹೀ",
            "ಫು": "ಪ್ಹು",
            "ಫೂ": "ಪ್ಹೂ",
            "ಫೇ": "ಪ್ಹೇ",
            "ಫೋ": "ಪ್ಹೋ",
            "ಫ": "ಪ್ಹ",

            # jh's
            "ಝ": "ಜ್ಹ",
            "ಝಾ": "ಜ್ಹಾ",
            "ಝಿ": "ಜ್ಹಿ",
            "ಝೀ": "ಜ್ಹೀ",
            "ಝು": "ಜ್ಹು",
            "ಝೂ": "ಜ್ಹೂ",
            "ಝೇ": "ಜ್ಹೇ",
            "ಝೋ": "ಜ್ಹೋ",

        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text
