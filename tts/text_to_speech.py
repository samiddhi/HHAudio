import os
import azure.cognitiveservices.speech as speechsdk
from text_processors.text_processor import ITextProcessor


class TextToSpeech:
    def __init__(self, processor: ITextProcessor, voice: str, language: str):
        self.processor = processor
        self.voice = voice
        self.language = language
        self.speech_key = os.environ.get('AZURE_SPEECH_KEY')
        self.speech_region = os.environ.get('AZURE_REGION')

        if not self.speech_key or not self.speech_region:
            raise EnvironmentError("Ensure SPEECH_KEY and SPEECH_REGION are set in the environment variables.")

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.speech_region)
        self.speech_config.speech_synthesis_voice_name = self.voice
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

    def synthesize(self, text: str) -> bytes:
        # Process the text using the appropriate processor
        processed_text = self.processor.process_text(text)

        # Use SSML for more precise control over synthesis
        ssml_template = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.language}">
            <voice name="{self.voice}">
                {processed_text}
            </voice>
        </speak>
        """

        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(ssml_template).get()

        # Check if speech synthesis completed successfully
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized successfully.")
            return speech_synthesis_result.audio_data
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error and cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
            return None
