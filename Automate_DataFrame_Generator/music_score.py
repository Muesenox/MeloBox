class music_score:
    def __init__(self, num, beats, beat_type):
        self.num = num
        self.beats = beats
        if beat_type == 2: self.beat_type = 'half'
        elif beat_type == 4: self.beat_type = 'quarter'
        elif beat_type == 8: self.beat_type = 'eighth'
        elif beat_type == 16: self.beat_type = '16th'
        else: raise Exception('beat_type should be 2, 4, 8 or 16. The value of beat_type was: {}'.format(beat_type))
        self.name = 'Note'
        self.step = None
        self.octave = None
        self.note_type = None
        beat_time = [['whole', 1], ['half', 0.5], ['quarter', 0.25], ['eighth', 0.125], ['16th', 0.0625], ['32nd', 0.03125]]
        self.beat_time = [[e[0], beat_type*e[1]] for e in beat_time]
        self.time = None
        self.tied_stop = False
        self.dot = 0
    
    def __str__(self):
        return self.name + '-' + str(self.num) + '-' + self.note_type + '-dot' + str(self.dot) + '-Time' + str(self.time)
    
    def set_step(self, step):
        assert self.name is 'Note' or self.name is 'Tide_Stop_Note' or self.name is 'Chord' or self.name is 'Tied_Chord', 'name should be Note, Tide_Stop_Note or Chord or Tied_Chord. The value of name was: {}'.format(self.name) 
        self.step = step
    
    def set_octave(self, octave):
        assert self.name is 'Note' or self.name is 'Tide_Stop_Note' or self.name is 'Chord' or self.name is 'Tied_Chord', 'name should be Note, Tide_Stop_Note or Chord or Tied_Chord. The value of name was: {}'.format(self.name)
        self.octave = octave
    
    def convert_to_rest(self):
        self.name = 'Rest'
        self.step = None
        self.octave = None
        self.note_type = 'measure'
        self.time = self.beats
    
    def convert_to_tied_stop_note(self):
        self.name = 'Tied_Stop_Note'
        self.tied_stop = True
    
    def convert_to_chord(self):
        self.name = 'Chord'
    
    def convert_to_tied_chord(self):
        self.name = 'Tied_Chord'
    
    def add_dot(self):
        self.dot += 1
        self.time += (self.time / (2 * self.dot))

    
    def set_note_type(self, note_type):
        self.note_type = note_type
        for e in self.beat_time:
            if e[0] == note_type: self.time = e[1]
        if self.time is None: raise Exception('Invalid note_type. The value of note_type was: {}'.format(note_type))
    
    def get_score(self):
        score = str()
        score = self.name + '-' + self.note_type if self.name == 'Rest' else self.name + '-' + self.note_type + '-' + self.step + self.octave + '-dot' + str(self.dot)
        return score
    
    def get_octave(self):
        return self.octave
    
    def get_step(self):
        return self.step
    
    def get_type(self):
        return self.note_type
    
    def get_dot(self):
        return self.dot
    
    def get_time(self):
        return self.time
    
    def get_name(self):
        return self.name