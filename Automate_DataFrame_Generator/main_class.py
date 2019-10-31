from musicXML_reader import *
from music_score import *
import os
import pandas as pd

def main():
    path = str(input('Please identify your training_set path : '))
    inDir = os.chdir(path + '/musicXML_Files') # Select the directory
    file_names = os.listdir(inDir)
    whole_tempo = list()
    whole_beats = list()
    whole_beat_type = list()
    whole_gClef_score_series = list()
    whole_fClef_score_series = list()
    whole_gClef_onset = list()
    whole_fClef_onset = list()
    whole_gClef_score_onset = list()
    whole_fClef_score_onset = list()
    file_names.remove('.DS_Store')
    for e in file_names:
        score_gClef = musicXML_reader(path + '/musicXML_Files/' + e, 1)
        score_gClef.activate()
        score_series_gClef = score_gClef.get_score_series()
        onset_gClef = score_gClef.get_times_onset()
        score_onset_gClef = score_gClef.get_score_onset()
        tempo = score_gClef.get_tempo()
        beats = score_gClef.get_beats()
        beat_type = score_gClef.get_beat_type()
        score_fClef = musicXML_reader(path + '/musicXML_Files/' + e, 2)
        score_fClef.activate()
        score_series_fClef = score_fClef.get_score_series()
        onset_fClef = score_fClef.get_times_onset()
        score_onset_fClef = score_fClef.get_score_onset()
        whole_tempo.append(tempo)
        whole_beats.append(beats)
        whole_beat_type.append(beat_type)
        whole_gClef_score_series.append(score_series_gClef)
        whole_fClef_score_series.append(score_series_fClef)
        whole_gClef_onset.append(onset_gClef)
        whole_fClef_onset.append(onset_fClef)
        whole_gClef_score_onset.append(score_onset_gClef)
        whole_fClef_score_onset.append(score_onset_fClef)
    data_dict = {'File_Name':file_names, 'Tempo':whole_tempo, 'Beats':whole_beats, 'Beat_Type':whole_beat_type, 'G_Clef_Score':whole_gClef_score_series, 'F_Clef_Score':whole_fClef_score_series, 'G_Clef_Onset':whole_gClef_onset, 'F_Clef_Onset':whole_fClef_onset, 'G_Clef_Score&Onset':whole_gClef_score_onset, 'F_Clef_Score&Onset':whole_fClef_score_onset}
    data_frame = pd.DataFrame(data_dict)
    print('Data Frame : ', data_frame)
    os.chdir('..')
    export_csv = data_frame.to_csv('musicXML_data_frame.csv', index = None, header = True)

if __name__ == '__main__':
    main()