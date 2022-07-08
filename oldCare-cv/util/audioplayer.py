# -*- coding: utf-8 -*-
'''
audio player
'''

# import library
from subprocess import call
import pygame  #播放音频文件的方法


# play audio
def play_audio(audio_name):
    try:
        call('mpg321 ' + audio_name, shell=True) # use mpg321 player
        pygame.mixer.init()
        print(audio_name)
        pygame.mixer.music.load(audio_name)
        pygame.mixer.music.play() #完成加载以及播放

    except KeyboardInterrupt as e:
        print(e)
    finally:
        pass

if __name__ == '__main__':
    pass
    
