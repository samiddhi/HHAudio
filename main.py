import uuid
from datetime import datetime
from text_processors.pali_text_processor import PaliTextProcessor
from text_processors.english_text_processor import EnglishTextProcessor
from tts.text_to_speech import TextToSpeech
from tools.file_utils import save_audio

def test(lang):
    if lang == "pi" or lang == "both":
        # Pali text processing
        pali_processor = PaliTextProcessor()
        pali_tts = TextToSpeech(processor=pali_processor, voice="en-US-BrandonMultilingualNeural", language="kn-IN")
        pali_audio = pali_tts.synthesize("evaṃ me sutaṃ — ekaṃ samayaṃ bhagavā sāvatthiyaṃ viharati jetavane anāthapiṇḍikassa ārāme")
        if pali_audio:
            # Use a timestamp and UUID for a unique filename
            pali_filename = f"pali_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.wav"
            save_audio(pali_audio, pali_filename)

    if lang == "en" or lang == "both":
        # English text processing
        english_processor = EnglishTextProcessor()
        english_tts = TextToSpeech(processor=english_processor, voice="en-US-BrianMultilingualNeural", language="en-US")
        english_audio = english_tts.synthesize("Thus have I heard. On one occasion the Blessed One was living at Sāvatthī in Jeta’s Grove, Anāthapiṇḍika’s Park.")
        if english_audio:
            # Use a timestamp and UUID for a unique filename
            english_filename = f"english_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.wav"
            save_audio(english_audio, english_filename)

if __name__ == "__main__":
    test("en")