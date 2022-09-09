#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
import moviepy.editor as mpy
import numpy as np
import pandas as pd
import cv2
from tqdm.auto import tqdm
from os import mkdir, listdir
from os.path import exists, join
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

def create_gesture_combinations(pairings, files, is_1G=False):
    for ind, pair in enumerate(pairings):
        gestures_left = []
        gestures_right = []
        if is_1G: # for the 1G condition only extract one gesture per side (the other side will be 'gg00' in each case)
            regex_left = rf'({pair[0]})_(f01|p)'
            regex_right = rf'({pair[1]})_(f02|n)'
        else: # for 2G condition extract both gesture per side (to allow for SAME and DIFF combinations)
            regex_left = rf'({pair[0]}|{pair[1]})_(f01|p)'
            regex_right = rf'({pair[0]}|{pair[1]})_(f02|n)'

        # get the filenames for the gestures to be paired
        for f in files:
            if search(regex_left, f):
                gestures_left.append(f)
            elif search(regex_right, f):
                gestures_right.append(f)
        # calculate all desired combinations for the respective pairing
        pairings[ind] = [(left,right) for right in gestures_right for left in gestures_left]

    return pairings

def determine_interaction_type(left, right):
    # from the naming of the individual stimuli files determine which interaction type the output file will have
    if len(left[33:-4]) != len(right[33:-4]):
        return 'HR'
    elif len(left[33:-4]) == 1:
        return 'RR'
    else:
        return 'HH'

def determine_gesture_type(left, right):
    # from the naming of the individual stimuli files determine which gesture type the output file will have
    if left[28:32] == 'gg00':
        return '1G'
    elif left[28:32] != right[28:32]:
        return '2G_DIFF'
    else:
        return '2G_SAME'

def main():
    in_dir = 'IndividualStimuliCleaned'
    files = [join(in_dir, f) for f in listdir(in_dir)]

    root_dir = 'DyadStimuli'
    sub_dirs = ['1G', '2G_SAME', '2G_DIFF'] # Single-passive-gestures; Two-identical-gestures; Two-different-gestures (gesture types)
    sub_sub_dirs = ['HH','HR','RR'] # Human-Human-Interaction; Human-Robot-Interaction; Robot-Robot-Interaction (interaction types)

    # create the folder structure of the output directory
    is_existend = exists(root_dir)
    if not is_existend:
        mkdir(root_dir)
        for sub_dir in sub_dirs:
            path_sub_dir = join(root_dir,sub_dir)
            mkdir(path_sub_dir)
            for sub_sub_dir in sub_sub_dirs:
                path_sub_sub_dir = join(root_dir,sub_dir,sub_sub_dir)
                mkdir(path_sub_sub_dir)

    # get all congruent 2G pairings
    pairings_2G = [('gg09', 'gg19'), ('gg01', 'gg18'), ('gg10', 'gg11'), ('gg13', 'gg17'),
                   ('gg08', 'gg20'), ('gg04', 'gg15'), ('gg02', 'gg06'), ('gg03', 'gg07'),]

    # get all 1G pairings
    all_gestures_df = pd.read_excel('GesturesIndividualStimuli.xlsx', 'gestures_combinations')
    relevant_gestures_df = all_gestures_df.dropna()
    gesture_codes = relevant_gestures_df['GestureCode'].tolist()

    pairings_1G = []
    for i in gesture_codes[1:]:
        single_gesture = ('gg00', i)
        pairings_1G.append(single_gesture)

    # create all combinations for the 1G and 2G pairings
    combinations_2G = create_gesture_combinations(pairings_2G, files)
    combinations_1G = create_gesture_combinations(pairings_1G, files, True)
    all_combinations = combinations_2G + combinations_1G
    all_combs_flat = [item for sublist in all_combinations for item in sublist]

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
        duration = 3
        gesture_right = change_dur(gesture_right,duration)
        gesture_left = change_dur(gesture_left,duration)

        # load the background image
        background = mpy.ImageClip('background_dyads.png',duration=duration)

        # create the video composition
        dyad = mpy.CompositeVideoClip([background,
                                       gesture_left.set_position((660-center_left[0],background.size[1]-gesture_left.size[1]-170)),
                                       gesture_right.set_position((1260-center_right[0],background.size[1]-gesture_right.size[1]-170))
                                      ])
        # make the video grayscale
        dyad = dyad.fx(mpy.vfx.blackwhite)

        # write the output video file
        out_path = join(root_dir,gesture_type,interaction_type,f'DS_l{gestures[0][28:-4]}_r{gestures[1][28:-4]}.mp4')
        dyad.write_videofile(out_path,fps=25,audio=False, verbose=False, logger=None)

if __name__ == "__main__":
    main()
