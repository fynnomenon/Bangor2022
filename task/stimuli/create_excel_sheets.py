#!/usr/bin/env python
# coding: utf-8

import moviepy.editor as mpy
from os import walk
from os.path import join
import pandas as pd
from openpyxl import load_workbook

def create_dict(column_names):
    data_dict = {}
    for col_name in column_names:
        data_dict[col_name] = []

    return data_dict


individuals_dir = 'IndividualStimuliCleaned'
dyads_dir = 'DyadStimuli'
catch_dir = 'DyadStimuliCatch'

column_names_individuals = ['FilePath','FileName','FPS','Duration','Size','GestureCode','Actor']
column_names_dyads = ['FilePath','FileName','FPS','Duration','Size','GestureCodeLeft','GestureCodeRight','ActorLeft','ActorRight','PairingType','InteractionType']

individuals_dict = create_dict(column_names_individuals)
dyads_dict = create_dict(column_names_dyads)
catch_dict = create_dict(column_names_dyads)

dirs = [individuals_dir, dyads_dir, catch_dir]
dicts = [individuals_dict, dyads_dict, catch_dict]

for directory, dictionary in zip(dirs, dicts):
    for subdir, dirs, files in walk(directory):
        for f in files:
            dictionary['FileName'].append(f)

            file_path = join(subdir, f)
            dictionary['FilePath'].append(file_path)

            clip = mpy.VideoFileClip(file_path,has_mask=True)

            duration = clip.duration
            dictionary['Duration'].append(duration)

            fps = clip.fps
            dictionary['FPS'].append(fps)

            size = clip.size
            dictionary['Size'].append(size)

            if directory == individuals_dir:
                gesture = f[3:7]
                dictionary['GestureCode'].append(gesture)

                actor = f[8:-4]
                dictionary['Actor'].append(actor)
            else:
                string_parts = f.split('_')
                actor_right = string_parts[4][:-4]
                actor_left = string_parts[2]
                gesture_right = string_parts[3][1:]
                gesture_left = string_parts[1][1:]


                dictionary['GestureCodeLeft'].append(gesture_left)
                dictionary['ActorLeft'].append(actor_left)
                dictionary['GestureCodeRight'].append(gesture_right)
                dictionary['ActorRight'].append(actor_right)

                interaction_type = ''
                if len(actor_left) == len(actor_right):
                    interaction_type = 'HH'
                else:
                    interaction_type = 'HR'

                dictionary['InteractionType'].append(interaction_type)

                pairing_type = ''
                if gesture_left == gesture_right:
                    pairing_type = '2G_SAME'
                elif 'gg00' in [gesture_left, gesture_right]:
                    pairing_type = '1G'
                else:
                    pairing_type = '2G_DIFF'
                
                dictionary['PairingType'].append(pairing_type)


df_individuals = pd.DataFrame(individuals_dict).sort_values(by=['GestureCode', 'Actor']).reset_index(drop=True)
df_dyads = pd.DataFrame(dyads_dict).sort_values(by=['GestureCodeLeft', 'ActorLeft', 'GestureCodeRight', 'ActorRight']).reset_index(drop=True)
df_catch = pd.DataFrame(catch_dict).sort_values(by=['GestureCodeLeft', 'ActorLeft', 'GestureCodeRight', 'ActorRight']).reset_index(drop=True)

# Generating workbook
excel_workbook = load_workbook('AllStimuliFiles.xlsx')
 
# Generating the writer engine
writer = pd.ExcelWriter('AllStimuliFiles.xlsx', engine = 'openpyxl')
 
# Assigning the workbook to the writer engine
writer.book = excel_workbook

df_individuals.to_excel(writer, sheet_name = 'InvidualStimuliFiles')
df_dyads.to_excel(writer, sheet_name = 'DyadStimuliFiles')
df_catch.to_excel(writer, sheet_name = 'CatchStimuliFiles')

writer.save()
writer.close()





