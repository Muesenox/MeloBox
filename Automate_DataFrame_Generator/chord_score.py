from music_score import *

class chord_score:
    def __init__(self, note1, note2):
        self.note_list = [note1, note2]
        self.time = note1.get_time()
    
    def addNote(self, note):
        self.note_list.append(note)

    def __str__(self):
        str_notes = ''
        for i in range(len(self.note_list)):
            if i < len(self.note_list) - 1: str_notes += (self.note_list[i].get_score() + '-')
            else: str_notes += self.note_list[i].get_score()
        return 'Chord[' + str_notes + ']'
    
    def get_score(self):
        str_notes = ''
        for i in range(len(self.note_list)):
            if i < len(self.note_list) - 1: str_notes += (self.note_list[i].get_score() + '+')
            else: str_notes += self.note_list[i].get_score()
        return 'Chord_[' + str_notes + ']'
    
    def get_name(self):
        return 'Chord'
    
    def get_time(self):
        return self.time