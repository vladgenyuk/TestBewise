from pydub import AudioSegment


def convert(filename: str, ext: str):
    sound = AudioSegment.from_wav(f'files/{filename}.{ext}')
    sound.export(f'files/{filename}.mp3', format='mp3')

convert('game_over', 'wav')