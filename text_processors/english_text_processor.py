import re
from text_processors.text_processor import ITextProcessor
from tools.ipa import convert_uni_to_ipa

class EnglishTextProcessor(ITextProcessor):
    def process_text(self, text: str) -> str:

        # Overrides untranslated_terms
        self.manual_replacements = {
            "bhikkhus": "bʰikkʰuz",
            "sāvatthī": "sɑːʋətt̪ʰiː",
            "blessed": "ˈblɛsɪd"
        }

        self.untranslated_terms = [
            "bhikkhu",
            "saṅgha",
            "buddha",
            "sāvatthī",
            "anāthapiṇḍika",
            "jeta"
        ]

        text = self.replace_with_phoneme_tags(text)

        # Normalize white spaces (multiple spaces to one)
        text = re.sub(r'\s+', ' ', text)

        return text

    def replace_with_phoneme_tags(self, text):
        # Create a regular expression pattern to match terms in untranslated_terms and manual_replacements with optional "'s" suffix
        pattern = r'\b(' + '|'.join(re.escape(term) for term in self.untranslated_terms + list(self.manual_replacements.keys())) + r')(’s|\'s)?\b'

        def replacer(match):
            word = match.group(1)  # Get the word part (without "'s" or "’s")
            possessive = match.group(2)  # Get the "'s" or "’s" if it exists

            # Check if the word exists in manual_replacements first, case-insensitively
            word_lower = word.lower()

            # If it's in manual_replacements, use its IPA value
            if word_lower in self.manual_replacements:
                ipa = self.manual_replacements[word_lower]  # Use manual replacement IPA
            else:
                # Fallback to convert_uni_to_ipa function for untranslated terms
                ipa = convert_uni_to_ipa(word, "ipa")

            # Append 'z' if the word has "'s" or "’s"
            if possessive:
                ipa += 'z'

            # Create the SSML phoneme tag with the possessive part included in the replacement text
            phoneme_tag = f'<phoneme alphabet="ipa" ph="{ipa}">{word}{possessive if possessive else ""}</phoneme>'
            return phoneme_tag

        # Use re.sub to replace the matches in the text with phoneme tags, case-insensitively
        return re.sub(pattern, replacer, text, flags=re.IGNORECASE)
