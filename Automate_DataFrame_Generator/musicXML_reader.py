from music_score import *
from chord_score import *

class musicXML_reader:
    def __init__(self, file_name, staff):
        self.file_name = file_name
        self.staff = staff
        self.sequence = list()
        self.tempo = 120.0
        self.beats = int()
        self.beat_type = int()
        self.onset = [0]
        self.score_onset = list()
        self.score_series = list()
        self.sharp_accidental = ('F', 'C', 'G', 'D', 'A', 'E', 'B')
        self.flat_accidental = ('B', 'E', 'A', 'D', 'G', 'C', 'F')
        self.key_signature = list()
        self.fifths_mode = 0
    
    def activate(self):
        infile = open(self.file_name, 'r')
        index = 0
        note_tmp = list()
        detect_note = False
        repeat_sequence = list()
        repeat_able = False
        i = 0
        for line in infile:
            tmp = line.strip()
            if '<sound tempo=' in tmp: self.tempo = float(tmp[14:len(tmp) - 3])
            if '<fifths>' in tmp:
                self.fifths_mode = int(tmp[8:-9])
                if self.fifths_mode > 0: self.key_signature = [self.sharp_accidental[i] for i in range(abs(self.fifths_mode))]
                elif self.fifths_mode < 0: self.key_signature = [self.flat_accidental[i] for i in range(abs(self.fifths_mode))]
                else: self.key_signature = list()
            if '<beats>' in tmp: self.beats = int(tmp[7])
            if '<beat-type>' in tmp: self.beat_type = int(tmp[11])
            if '<repeat direction="forward"/>' in tmp: repeat_able = True
            if '<ending number="1" type="start"' in tmp: repeat_able = False
            if '<ending number="2" type="start"' in tmp:
              self.sequence += repeat_sequence
              repeat_sequence = list()
            if '<note' in tmp and not(detect_note):
                note_tmp.append(index)
                detect_note = True
            if tmp == '<rest/>': note_tmp.append(tmp)
            if tmp == '<chord/>': note_tmp.append(tmp)
            if '<step>' in tmp and detect_note: note_tmp.append(tmp)
            if '<octave>' in tmp and detect_note: note_tmp.append(tmp)
            if '<type>' in tmp and detect_note: note_tmp.append(tmp)
            if '<dot/>' in tmp and detect_note: note_tmp.append(tmp)
            if '<staff>' in tmp and detect_note: note_tmp.append(tmp)
            if '<tied type="stop"/>' in tmp and detect_note: note_tmp.append(tmp)
            if '</note>' in tmp and detect_note:
                iden_staff = '<staff>' + str(self.staff) + '</staff>'
                if note_tmp.count(iden_staff) == 1:
                    score = music_score(note_tmp[0], self.beats, self.beat_type)
                    for i in range(1, len(note_tmp)):
                        if note_tmp[i] == '<rest/>': score.convert_to_rest()
                        elif note_tmp[i] == '<chord/>': score.convert_to_chord()
                        if '<step>' in note_tmp[i]:
                            if self.fifths_mode < 0 and note_tmp[i][6] in self.key_signature: score.set_step(note_tmp[i][6] + 'b')
                            elif self.fifths_mode > 0 and note_tmp[i][6] in self.key_signature: score.set_step(note_tmp[i][6] + '#')
                            else: score.set_step(note_tmp[i][6])
                        if '<octave>' in note_tmp[i]: score.set_octave(note_tmp[i][8])
                        if '<type>' in note_tmp[i]: score.set_note_type(note_tmp[i][6:-7])
                        if '<dot/>' == note_tmp[i]: score.add_dot()
                        if '<tied type="stop"/>' == note_tmp[i]:
                            if score.get_name() == 'Chord': score.convert_to_tied_chord()
                            else: score.convert_to_tied_stop_note()
                    self.sequence.append(score)
                    if repeat_able: repeat_sequence.append(score)
                    index += 1
                note_tmp = list()
                detect_note = False
            i += 1
        tmp = self.sequence
        self.sequence = self.chord_generator(tmp)

    def chord_generator(self, sequence):
        out_sequence = list()
        pointer = 0
        pivot = 1
        while pointer < len(sequence):
            if pivot < len(sequence):
                if sequence[pivot].get_name() == 'Chord':
                    chord = chord_score(sequence[pointer], sequence[pivot])
                    pivot += 1
                    if pivot < len(sequence):
                        while sequence[pivot].get_name() == 'Chord':
                            chord.addNote(sequence[pivot])
                            pivot += 1
                            if pivot >= len(sequence): break
                    out_sequence.append(chord)
                    pointer = pivot
                    pivot += 1
                else:
                    out_sequence.append(sequence[pointer])
                    pivot += 1
                    pointer += 1
            else:
                out_sequence.append(sequence[pointer])
                break
        return out_sequence

    def get_sequence(self):
        return self.sequence
    
    def get_tempo(self):
        return self.tempo
    
    def get_beats(self):
        return self.beats
    
    def get_beat_type(self):
        return self.beat_type
    
    def get_times_onset(self):
        if len(self.onset) == 1:
            time = 0
            self.score_onset.append('0' + ':' + self.sequence[0].get_score())
            spb = 60 / self.tempo  # spd = sec per beat
            for i in range(len(self.sequence)):
                if self.sequence[i].get_name() == 'Tied_Stop_Note' or self.sequence[i].get_name() == 'Rest':
                    update = (self.sequence[i].get_time() * spb)
                    time += update
                    self.onset[-1] += update
                elif self.sequence[i].get_name() == 'Note' or self.sequence[i].get_name() == 'Chord':
                    time += (self.sequence[i].get_time() * spb)
                    self.onset.append(time)
                    self.score_onset.append(str(time) + ':' + self.sequence[i].get_score())
            self.onset.pop(-1)
        return self.onset
    
    def get_score_series(self):
        if len(self.score_series) == 0:
            for e in self.sequence: self.score_series.append(e.get_score())
        return self.score_series

    def get_score_onset(self):
        return self.score_onset