from Clicks_Generator import *

def main():
    dataFrame = pd.read_csv('/Users/muesenox/Documents/Graduation_Project/training_set/musicXML_data_frame.csv')
    selected_music = int(input('Enter music No. : '))
    selected_series = dataFrame.iloc[selected_music]    # Selected row
    g_clef_str_score = selected_series[8]               # Selected column
    g_clef_str_score = g_clef_str_score[1:-1]
    f_clef_str_score = selected_series[9]
    f_clef_str_score = f_clef_str_score[1:-1]
    cg = Clicks_Generator(g_clef_str_score, f_clef_str_score)
    cg.activate()
    cg.write_wav('test_musicbox', '/Users/muesenox/Documents/Graduation_Project/training_set/Output_of_CG/')

if __name__ == '__main__':
    main()