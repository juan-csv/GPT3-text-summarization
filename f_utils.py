from pydub import AudioSegment

def mp3_to_wav(audio_file_path):
    sound = AudioSegment.from_mp3(audio_file_path)
    audio_file_path = audio_file_path.split('.')[0] + '.wav'
    sound.export(audio_file_path, format="wav")
    return audio_file_path

#audio_file_path = mp3_to_wav("audio_data_donald_trump_fake_0ghm5Cqpfwk.mp3")
#print(audio_file_path)
