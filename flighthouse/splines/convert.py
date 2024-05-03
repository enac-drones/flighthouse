import pandas as pd
file_path = 'splines/liste_mot.csv'
data = pd.read_csv(file_path, sep=',')
#replace items in japanese_audio column with the wav extension instead of ogg
data['japanese_audio'] = data['japanese_audio'].str.replace('.ogg', '.wav')

#save the modified data to a new csv file
data.to_csv('splines/liste_mot_wav.csv', index=False)

