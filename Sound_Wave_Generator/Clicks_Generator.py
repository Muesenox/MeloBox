import librosa
import pandas as pd
import numpy as np

class Clicks_Generator:
    def __init__(self, g_clef_music_score_and_onset, f_clef_music_score_and_onset):
        self.note_frequencies = {'A0':None, 'A#0':None, 'Bb0':None, 'B0':None, 'C1':None, 'C#1':None, 'Db1':None, 'D1':None, 'D#1':None, 'Eb1':None,
        'E1':None, 'F1':None, 'F#1':None, 'Gb1':None, 'G1':None, 'G#1':None, 'Ab1':None, 'A1':None, 'A#1':None, 'Bb1':None, 'B1':None, 'C2':None,
        'C#2':None, 'Db2':None, 'D2':None, 'D#2':None, 'Eb2':None, 'E2':None, 'F2':None, 'F#2':None, 'Gb2':None, 'G2':None, 'G#2':None,
        'Ab2':None, 'A2':None, 'A#2':None, 'Bb2':None, 'B2':None, 'C3':None, 'C#3':None, 'Db3':None, 'D3':None, 'D#3':None, 'Eb3':None,
        'E3':None, 'F3':None, 'F#3':None, 'Gb3':None, 'G3':None, 'G#3':None, 'Ab3':None, 'A3':None, 'A#3':None, 'Bb3':None, 'B3':None, 'C4':None,
        'C#4':None, 'Db4':None, 'D4':None, 'D#4':None, 'Eb4':None, 'E4':None, 'F4':None, 'F#4':None, 'Gb4':None, 'G4':None, 'G#4':None,
        'Ab4':None, 'A4':None, 'A#4':None, 'Bb4':None, 'B4':None, 'C5':None, 'C#5':None, 'Db5':None, 'D5':None, 'D#5':None, 'Eb5':None,
        'E5':None, 'F5':None, 'F#5':None, 'Gb5':None, 'G5':None, 'G#5':None, 'Ab5':None, 'A5':None, 'A#5':None, 'Bb5':None, 'B5':None,
        'C6':None, 'C#6':None, 'Db6':None, 'D6':None, 'D#6':None, 'Eb6':None, 'E6':None, 'F6':None, 'F#6':None, 'Gb6':None, 'G6':None,
        'G#6':None, 'Ab6':None, 'A6':None, 'A#6':None, 'Bb6':None, 'B6':None, 'C7':None, 'C#7':None, 'Db7':None, 'D7':None, 'D#7':None,
        'Eb7':None, 'E7':None, 'F7':None, 'F#7':None, 'Gb7':None, 'G7':None, 'G#7':None, 'Ab7':None, 'A7':None, 'A#7':None, 'Bb7':None,
        'B7':None, 'C8':None}
        self.pitch = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        g_clef_score = g_clef_music_score_and_onset.split(',')
        for i in range(len(g_clef_score)):
            tmp = g_clef_score[i].split(':')
            tmp[0] = float(tmp[0].strip()[1:])
            tmp[1] = tmp[1][:-1]
            g_clef_score[i] = tmp
        self.g_clef_score = g_clef_score
        f_clef_score = f_clef_music_score_and_onset.split(',')
        for i in range(len(f_clef_score)):
            tmp = f_clef_score[i].split(':')
            tmp[0] = float(tmp[0].strip()[1:])
            tmp[1] = tmp[1][:-1]
            f_clef_score[i] = tmp
        self.f_clef_score = f_clef_score
        self.wave = None
    
    def activate(self):
        len_wave = int(self.g_clef_score[-1][0] + 1) * 22050 if (self.g_clef_score[-1][0] > self.f_clef_score[-1][0]) else int(self.f_clef_score[-1][0] + 1) * 22050
        wave = np.ndarray(len_wave)
        for e in self.g_clef_score:
            info = e[1].split('_')
            if len(info) == 1:
                step = info[0].split('-')
                if step[0] == 'Note':
                    if str(type(self.note_frequencies[step[2]])) == "<class 'NoneType'>":
                        f_name = self.pitch[self.pitch.index(step[2][0]) + 1] + 'b' + step[2][2] if step[2][1] == '#' else step[2]
                        pitch, pitch_sr = librosa.load('/Users/muesenox/Documents/Graduation_Project/MIDI_Generator/note_signals/' + f_name + '.mp3')
                        if len(step[2]) > 2:
                            if step[2][1] == '#':
                                self.note_frequencies[step[2]] = pitch
                                index = self.pitch.index(step[2][0])
                                self.note_frequencies[self.pitch[index + 1] + 'b' + step[2][2]] = pitch
                            else:
                                self.note_frequencies[step[2]] = pitch
                                index = self.pitch.index(step[2][0])
                                self.note_frequencies[self.pitch[index - 1] + '#' + step[2][2]] = pitch
                        else:
                            self.note_frequencies[step[2]] = pitch
                    clicks = librosa.clicks(times = [e[0]], sr = 22050, length = len_wave, click = self.note_frequencies[step[2]])
                    wave += clicks
            else:
                tmp = info[1][1:-1]
                step = tmp.split('+')
                for i in range(len(step)): step[i] = step[i].split('-')
                for note in step:
                    if str(type(self.note_frequencies[note[2]])) == "<class 'NoneType'>":
                        f_name = self.pitch[self.pitch.index(note[2][0]) + 1] + 'b' + note[2][2] if note[2][1] == '#' else note[2]
                        pitch, pitch_sr = librosa.load('/Users/muesenox/Documents/Graduation_Project/MIDI_Generator/note_signals/' + f_name + '.mp3')
                        if len(note[2]) > 2:
                            if note[2][1] == '#':
                                self.note_frequencies[note[2]] = pitch
                                index = self.pitch.index(note[2][0])
                                self.note_frequencies[self.pitch[index + 1] + 'b' + note[2][2]] = pitch
                            else:
                                self.note_frequencies[note[2]] = pitch
                                index = self.pitch.index(note[2][0])
                                self.note_frequencies[self.pitch[index - 1] + '#' + note[2][2]] = pitch
                        else:
                            self.note_frequencies[note[2]] = pitch
                    clicks = librosa.clicks(times = [e[0]], sr = 22050, length = len_wave, click = self.note_frequencies[note[2]])
                    wave += clicks
        self.wave = wave
        wave = np.ndarray(len_wave)
        for e in self.f_clef_score:
            info = e[1].split('_')
            if len(info) == 1:
                step = info[0].split('-')
                if step[0] == 'Note':
                    if str(type(self.note_frequencies[step[2]])) == "<class 'NoneType'>":
                        f_name = self.pitch[self.pitch.index(step[2][0]) + 1] + 'b' + step[2][2] if step[2][1] == '#' else step[2]
                        pitch, pitch_sr = librosa.load('/Users/muesenox/Documents/Graduation_Project/MIDI_Generator/note_signals/' + f_name + '.mp3')
                        if len(step[2]) > 2:
                            if step[2][1] == '#':
                                self.note_frequencies[step[2]] = pitch
                                index = self.pitch.index(step[2][0])
                                self.note_frequencies[self.pitch[index + 1] + 'b' + step[2][2]] = pitch
                            else:
                                self.note_frequencies[step[2]] = pitch
                                index = self.pitch.index(step[2][0])
                                self.note_frequencies[self.pitch[index - 1] + '#' + step[2][2]] = pitch
                        else:
                            self.note_frequencies[step[2]] = pitch
                    clicks = librosa.clicks(times = [e[0]], sr = 22050, length = len_wave, click = self.note_frequencies[step[2]])
                    wave += clicks
            else:
                tmp = info[1][1:-1]
                step = tmp.split('+')
                for i in range(len(step)): step[i] = step[i].split('-')
                for note in step:
                    if str(type(self.note_frequencies[note[2]])) == "<class 'NoneType'>":
                        f_name = self.pitch[self.pitch.index(note[2][0]) + 1] + 'b' + note[2][2] if note[2][1] == '#' else note[2]
                        pitch, pitch_sr = librosa.load('/Users/muesenox/Documents/Graduation_Project/MIDI_Generator/note_signals/' + f_name + '.mp3')
                        if len(note[2]) > 2:
                            if note[2][1] == '#':
                                self.note_frequencies[note[2]] = pitch
                                index = self.pitch.index(note[2][0])
                                self.note_frequencies[self.pitch[index + 1] + 'b' + note[2][2]] = pitch
                            else:
                                self.note_frequencies[note[2]] = pitch
                                index = self.pitch.index(note[2][0])
                                self.note_frequencies[self.pitch[index - 1] + '#' + note[2][2]] = pitch
                        else:
                            self.note_frequencies[note[2]] = pitch
                    clicks = librosa.clicks(times = [e[0]], sr = 22050, length = len_wave, click = self.note_frequencies[note[2]])
                    wave += clicks
        wave = np.divide(wave, 1.25)
        self.wave += wave
        print('Music Box was completed.')
    
    def write_wav(self, file_name, path):
        librosa.output.write_wav(path + file_name + '.mp3', self.wave, 22050)
