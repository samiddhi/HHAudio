import os

def save_audio(audio_data: bytes, filename: str, directory: str = "generated_audio") -> None:
    """
    Save audio data to a file.

    :param audio_data: The audio data as bytes.
    :param filename: The desired filename.
    :param directory: The directory where the file should be saved.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Save the audio file
    file_path = os.path.join(directory, filename)
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)
    print(f"Audio saved to {file_path}")