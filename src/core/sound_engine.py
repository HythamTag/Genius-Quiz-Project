import time
import winsound

from pygame import mixer
import pygame
pygame.init()

class Sound_Action:
    @staticmethod
    def play_song(file_path):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()

    @staticmethod
    def stop_song():
        try:
            mixer.music.unload()
            mixer.music.stop()
        except:
            pass

    @staticmethod
    def sound_Correct():
        winsound.PlaySound("Sources/ui/Resources/sounds/sound_Correct.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_Wrong():
        winsound.PlaySound("Sources/ui/Resources/sounds/sound_Wrong.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_Start20():
        winsound.PlaySound("Sources/ui/Resources/sounds/Sound_Start20.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_timeout():
        winsound.PlaySound("Sources/ui/Resources/sounds/Sound_End.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_time4():
        winsound.PlaySound("Sources/ui/Resources/sounds/Sound_Time.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_Start45():
        winsound.PlaySound("Sources/ui/Resources/sounds/Sound_Start45.wav", winsound.SND_ASYNC)

    @staticmethod
    def sound_Buzzer():
        winsound.PlaySound("Sources/ui/Resources/sounds/Sound_Buzzer.wav", winsound.SND_ASYNC)
        time.sleep(1)

    @staticmethod
    def sound_Background(play):
        if play:
            winsound.PlaySound("Sources/ui/Resources/Movies/back_music.wav", winsound.SND_ASYNC)
        elif play is False:
            winsound.PlaySound(None, winsound.SND_PURGE)

def main():

    Sound_Action.play_song('Data/Episode_1/Alan Walker - Faded_[Historical,3,0].mp3')
    # time.sleep(5)
    Sound_Action.stop_song()
    index = 0
    while 1:
        index += 1
        print(index)


if __name__ == '__main__':
    main()

# from pydub import AudioSegment
# from pydub.playback import play
#
# audio1 = AudioSegment.from_file("chunk1.wav") #your first audio file
# audio2 = AudioSegment.from_file("chunk2.wav") #your second audio file
# audio3 = AudioSegment.from_file("chunk3.wav") #your third audio file
#
# mixed = audio1.overlay(audio2)          #combine , superimpose audio files
# mixed1  = mixed.overlay(audio3)          #Further combine , superimpose audio files
# #If you need to save mixed file
# mixed1.export("mixed.wav", format='wav') #export mixed  audio file
# play(mixed1)                             #play mixed audio file

