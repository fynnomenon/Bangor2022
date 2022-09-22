#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
import moviepy.editor as mpy
import numpy as np
import pandas as pd
import cv2
import shutil
import random
from tqdm.auto import tqdm
from os import mkdir, makedirs, listdir, walk
from os.path import join
from re import search
from crop_and_resize import get_bbox_coords

def change_dur(clip, duration):
    rate = clip.fps
    dur = clip.duration

    desired_rate = (rate*dur)/duration
    scaling_factor = desired_rate/rate

    # modify the FPS
    clip = clip.set_fps(clip.fps*scaling_factor)
    # apply speed up
    clip = clip.fx(mpy.vfx.speedx,scaling_factor)

    return clip

def calculate_center(clip):
    x,y,w,h = get_bbox_coords(clip)
    center = (round((2*x+w)/2),round((2*y+h)/2))

    return center

def create_folder_structure(root_dirs, sub_dirs, sub_sub_dirs):
    directories = [join(root_dir, sub_dir, sub_sub_dir) for sub_sub_dir in sub_sub_dirs for sub_dir in sub_dirs for root_dir in root_dirs]
    for directory in directories:
        makedirs(directory)

def determine_interaction_type(left, right):
    # from the naming of the individual stimuli files determine which interaction type the output file will have
    if len(left[33:-4]) != len(right[33:-4]):
        return 'HR'
    else:
        return 'HH'

def determine_gesture_type(left, right):
    # from the naming of the individual stimuli files determine which gesture type the output file will have
    if 'gg00' in [left[28:32], right[28:32]]:
        return '1G'
    elif left[28:32] != right[28:32]:
        return '2G_DIFF'
    else:
        return '2G_SAME'

def create_gesture_combinations(pairings, files, interaction_type='HH'):
    combs = []
    for ind, pair in enumerate(pairings):
        gestures_left = []
        gestures_right = []

        if interaction_type == 'HH':
            regex = rf'({pair[0]}|{pair[1]})_(f01|f02)'
        elif interaction_type == 'HR':
            regex = rf'({pair[0]}|{pair[1]})_(m02|p)'

        # get the filenames for the gestures to be paired
        for f in files:
            if search(regex, f):
                gestures_left.append(f)
                gestures_right.append(f)

        # calculate all desired combinations for the respective pairing
        temp_combs = [(left,right) for right in gestures_right for left in gestures_left if left[33:-4] != right[33:-4]]
        correct_combs = [pair for pair in temp_combs if not(determine_gesture_type(pair[0],pair[1]) == '1G' and pair[0][28:32] == pair[1][28:32])]
        combs.append(correct_combs)

    return combs

def main():
    # get a list of all files in the input directory
    in_dir = 'IndividualStimuliCleaned'
    files = [join(in_dir, f) for f in listdir(in_dir)]

    out_dir = 'DyadStimuli'
    seq_dir = 'ImageSequencesDyads'
    seq_dir_catch = 'ImageSequencesCatch'
    out_dir_catch = 'DyadStimuliCatch'
    root_dirs = [out_dir,out_dir_catch,seq_dir]
    sub_dirs = ['1G', '2G_SAME', '2G_DIFF'] # Single-passive-gestures; Two-identical-gestures; Two-different-gestures (gesture types)
    sub_sub_dirs = ['HH','HR'] # Human-Human-Interaction; Human-Robot-Interaction;

    create_folder_structure(root_dirs, sub_dirs, sub_sub_dirs)

    # get all 2G pairings
    pairings_2G = [('gg04', 'gg11'), ('gg18', 'gg01'), ('gg06', 'gg19'), ('gg08', 'gg20')]

    # get all 1G pairings
    all_gestures_df = pd.read_excel('GesturesIndividualStimuli.xlsx', 'gestures_combinations')
    relevant_gestures_df = all_gestures_df.dropna().drop([2,3,7,9,10,13,14,16])
    gesture_codes = relevant_gestures_df['GestureCode'].tolist()

    pairings_1G = []
    for i in gesture_codes[1:]:
        single_gesture = ('gg00', i)
        pairings_1G.append(single_gesture)

    all_pairings = pairings_2G + pairings_1G

    # create all combinations for the 1G and 2G pairings
    combinations_HH = create_gesture_combinations(all_pairings, files, 'HH')
    combinations_HR = create_gesture_combinations(all_pairings, files, 'HR')
    all_combinations = combinations_HH + combinations_HR
    all_combs_flat = {item for sublist in all_combinations for item in sublist}

    duration = 3

    for gestures in tqdm(all_combs_flat):
        # determine the interaction and gesture type of the dyad stimuli to be created
        interaction_type = determine_interaction_type(gestures[0],gestures[1])
        gesture_type = determine_gesture_type(gestures[0],gestures[1])

        # load the video files of the individual stimuli to be combined into a dyad
        gesture_left = mpy.VideoFileClip(gestures[0],has_mask=True)
        gesture_right = mpy.VideoFileClip(gestures[1],has_mask=True).fx(mpy.vfx.mirror_x)

        # calculate the center of gravity of the human body in the resized clip
        center_left = calculate_center(gesture_left)
        center_right = calculate_center(gesture_right)

        # speed up or slow down video to 3sec
        gesture_right = change_dur(gesture_right,duration)
        gesture_left = change_dur(gesture_left,duration)

        # load the background image
        background = mpy.ImageClip('background_transparent.png',duration=duration)

        # create the video composition
        dyad_seq = mpy.CompositeVideoClip([background,
                                       gesture_left.set_position((660-center_left[0],background.size[1]-gesture_left.size[1]-170)),
                                       gesture_right.set_position((1260-center_right[0],background.size[1]-gesture_right.size[1]-170))
                                      ])

        # Workaround for the moviepy bug that write_videofile() cannot export a video clip with an alpha channel
        img_seq_path = join(seq_dir,gesture_type,interaction_type,f'DS_l{gestures[0][28:-4]}_r{gestures[1][28:-4]}')
        mkdir(img_seq_path)
        dyad_seq.write_images_sequence(f'{img_seq_path}/frame%04d.png', fps=25, withmask=True, verbose=False, logger=None) # create image sequence of dyad vidoes

    #load the background image
    background = mpy.ImageClip('background_gray.png',duration=duration)

    for subdir, dirs, files in walk(seq_dir):
        if len(subdir) >= 31:
            dyad_transparent = mpy.ImageSequenceClip(subdir, fps=25)
            dyad = mpy.CompositeVideoClip([background, dyad_transparent])
            dyad.write_videofile(out_dir+subdir.split(seq_dir,1)[1]+'.mp4', fps=25)

    shutil.copytree(seq_dir, seq_dir_catch)

    left_right = [0,1]*int(128/2)
    random.shuffle(left_right)

    frm_count = 0

    for subdir, dirs, files in walk(seq_dir_catch):
        if len(subdir) >= 31:
            # generate random frame number (200ms after start and before the end of the clip)
            total_frms = 75
            rand_frm_num = random.randint(5, total_frms-5)
            for f in listdir(subdir):
                if search(rf'{rand_frm_num:04d}', f):
                    f_name = join(subdir, f)
                    frm = cv2.imread(f_name, cv2.IMREAD_UNCHANGED)

                    width = frm.shape[1]

                    if left_right[frm_count] == 0:
                        half_frm = frm[:,0:960,:]
                    else:
                        half_frm = frm[:,960:1920,:]

                    gray = cv2.cvtColor(half_frm, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray, (85,85), 0)
                    closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, (21,21))
                    thresh = cv2.threshold(closing, 1, 255, cv2.THRESH_BINARY)[1]

                    cnts = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
                    cv2.drawContours(half_frm, cnts, -1, color=(0,0,255,85), thickness=cv2.FILLED)

                    if left_right[frm_count] == 0:
                        frm[:,0:960,:] = half_frm
                    else:
                        frm[:,960:1920,:]  = half_frm

                    cv2.imwrite(f_name, frm)

                    frm_count += 1

            dyad_transparent = mpy.ImageSequenceClip(subdir, fps=25)
            dyad = mpy.CompositeVideoClip([background, dyad_transparent])
            dyad.write_videofile(out_dir_catch+subdir.split(seq_dir_catch,1)[1].replace('DS','Catch')+'.mp4', fps=25)

if __name__ == "__main__":
    main()
