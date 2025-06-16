import pygame as pg
import os

class SoundManager:
    def __init__(self, sounds_dir):
        self.sounds_dir = sounds_dir
        pg.mixer.init()

        self.sounds = {
            'warning': self._load_sound('warning.mp3'),
            'success': self._load_sound('success.mp3'),
            'failure': self._load_sound('failure.mp3'),
            'autosolve': self._load_sound('autosolve.mp3'),
        }

        self.background_tracks = [
            os.path.join(self.sounds_dir, 'background1.mp3'),
            os.path.join(self.sounds_dir, 'background2.mp3'),
        ]
        self.current_bg_index = 0

        self.BG_MUSIC_END = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.BG_MUSIC_END)

        self.background_looping = False  # looping flag

    def _load_sound(self, filename):
        return pg.mixer.Sound(os.path.join(self.sounds_dir, filename))

    def play(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()
        else:
            print(f"Sound '{sound_name}' not found!")

    def start_background_loop(self):
        self.background_looping = True  #  ENABLE LOOPING
        self._play_next_background()

    def _play_next_background(self):
        if not self.background_looping:
            return  #  DONT PLAY if looping was stopped
        pg.mixer.music.load(self.background_tracks[self.current_bg_index])
        pg.mixer.music.play(fade_ms=2000)
        self.current_bg_index = (self.current_bg_index + 1) % len(self.background_tracks)

    def handle_event(self, event):
        if event.type == self.BG_MUSIC_END and self.background_looping:
            self._play_next_background()

    def is_background_playing(self):
        return pg.mixer.music.get_busy()

    def stop_background_loop(self):
        self.background_looping = False  # ← DISABLE LOOPING
        pg.mixer.music.stop()
        self.current_bg_index = 0

    def set_volume(self, sound_name, volume):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.set_volume(volume)

    def stop(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.stop()
        else:
            print(f"Sound '{sound_name}' not found!")

    def cleanup(self):
        pg.mixer.quit()
