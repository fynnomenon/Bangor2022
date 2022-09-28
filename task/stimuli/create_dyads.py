#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
import moviepy.editor as mpy
import numpy as np
import cv2
import shutil
import random
import sys
from tqdm.auto import tqdm
from os import mkdir, makedirs, listdir, walk
from os.path import join
from re import search
from prepare_singles import get_bbox_coords
from get_stimuli_properties import create_sheet_dyads, create_sheet_catchTrials, get_gestures_and_actors_ind, get_pairing_type, get_interaction_type

def calculate_center(clip):
    # calculate the individual's center of mass from the bounding box of the first frame
    x,y,w,h = get_bbox_coords(clip)
    center = (round((2*x+w)/2),round((2*y+h)/2))

    return center

def create_folder_structure(root_dirs,sub_dirs,sub_sub_dirs):
    # create the folder structure for the outputs
    directories = [join(root_dir, sub_dir, sub_sub_dir) for sub_sub_dir in sub_sub_dirs for sub_dir in sub_dirs for root_dir in root_dirs]
    for directory in directories:
        makedirs(directory)

def create_gesture_combinations(pairings, in_dir, interaction_type, group):
    combs = []
    files = [join(in_dir, f) for f in listdir(in_dir)] # get a list of all files in the input directory
    ind_gesture_start, ind_gesture_end, ind_actor_start, ind_actor_end = get_gestures_and_actors_ind(in_dir)

    for ind, pair in enumerate(pairings):
        gestures_left = []
        gestures_right = []

        # change pairing of actors according to the group of the participant
        if group == 'A':
            actors = ['f01','f02','m02','p']
        elif group == 'B':
            actors = ['m02','f02','f01','p']
        else:
            actors = ['f01','m02','f02','p']
        # change regex according to the interaction type
        if interaction_type == 'HH':
            regex = rf'({pair[0]}|{pair[1]})_({actors[0]}|{actors[1]})'
        elif interaction_type == 'HR':
            regex = rf'({pair[0]}|{pair[1]})_({actors[2]}|{actors[3]})'

        # get the filenames for the gestures to be paired
        for f in files:
            if search(regex, f):
                gestures_left.append(f)
                gestures_right.append(f)

        # calculate all desired combinations for the respective pairing
        temp_combs = [(left,right) for right in gestures_right for left in gestures_left if left[ind_actor_start:ind_actor_end] != right[ind_actor_start:ind_actor_end]]
        correct_combs = [pair for pair in temp_combs if not(get_pairing_type(pair[0][ind_gesture_start:ind_gesture_end],pair[1][ind_gesture_start:ind_gesture_end]) == '1G' and pair[0][ind_gesture_start:ind_gesture_end] == pair[1][ind_gesture_start:ind_gesture_end])]
        combs.append(correct_combs)

    return combs

def add_glitch_effect(subdir, side, rand_frm_num, color, width, half_width):
    for f in listdir(subdir):
        if search(rf'{rand_frm_num:04d}', f):
            # read in the random frame
            f_name = join(subdir, f)
            frm = cv2.imread(f_name, cv2.IMREAD_UNCHANGED)

            # cut of the side of the frame which the glitch effect should not be apllied to
            if side == 'Left':
                half_frm = frm[:,0:half_width,:]
            else:
                half_frm = frm[:,half_width:width,:]

            # get the contours of the individual
            gray = cv2.cvtColor(half_frm, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (85,85), 0)
            closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, (21,21))
            thresh = cv2.threshold(closing, 1, 255, cv2.THRESH_BINARY)[1]
            cnts = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]

            # fill in the contours with the specified color
            cv2.drawContours(half_frm, cnts, -1, color, thickness=cv2.FILLED)

            if side == 'Left':
                frm[:,0:half_width,:] = half_frm
            else:
                frm[:,half_width:width,:]  = half_frm

            # overwrite the existing frame
            cv2.imwrite(f_name, frm)

def create_video(subdir, in_dir, out_dir, dir_thresh, background, duration, fps, dyad_name):
    dyad_transparent = mpy.ImageSequenceClip(subdir, fps=fps).set_duration(duration) # read pngs inside the directory as an ImageSequenceClip
    dyad = mpy.CompositeVideoClip([background, dyad_transparent]) # add a gray background to the video
    dyad.write_videofile(out_dir+dyad_name, fps=fps, verbose=False, logger=None) # create the dyad file

def main():
    # VARIABLES RELATED TO THE GROUP OF THE PARTICIPANT
    GROUP = str(sys.argv[1])

    # VARIABLES RELATED TO DIRECTORIES
    IN_DIR = 'Singles/Videos_Singles'
    OUT_DIR = 'Dyads/'+GROUP+'/Videos_Dyads'
    SEQ_DIR = 'Dyads/'+GROUP+'/ImageSequences_Dyads'
    SEQ_DIR_CATCH_LEFT = 'Dyads/'+GROUP+'/ImageSequences_CatchTrials_Left'
    SEQ_DIR_CATCH_RIGHT = 'Dyads/'+GROUP+'/ImageSequences_CatchTrials_Right'
    OUT_DIR_CATCH_LEFT = 'Dyads/'+GROUP+'/CatchTrials_Left'
    OUT_DIR_CATCH_RIGHT = 'Dyads/'+GROUP+'/CatchTrials_Right'
    ROOT_DIRS = [OUT_DIR,OUT_DIR_CATCH_LEFT,OUT_DIR_CATCH_RIGHT,SEQ_DIR]
    SUB_DIRS = ['1G', '2G_SAME', '2G_DIFF'] # Single-passive-gestures; Two-identical-gestures; Two-different-gestures (gesture types)
    SUB_SUB_DIRS = ['HH','HR'] # Human-Human-Interaction; Human-Robot-Interaction;

    # VARIABLES RELATED TO FILENAMES (depend on the naming convention of the files (for that refer to AllStimuliFiles.xlsx))
    IND_GESTURE_START,IND_GESTURE_END,IND_ACTOR_START,IND_ACTOR_END = get_gestures_and_actors_ind(IN_DIR)

    # VARIABLES RELATED TO PAIRINGS
    PAIRINGS_2G = [('gg01', 'gg18'), ('gg04', 'gg11'), ('gg06', 'gg19'), ('gg08', 'gg20')] # get all 2G pairings
    PAIRINGS_1G = [('gg00','gg01'), ('gg00','gg04'), ('gg00','gg06'), ('gg00','gg08'), # get all 1G pairings
                   ('gg00','gg11'), ('gg00','gg18'), ('gg00','gg19'), ('gg00','gg20')]
    #ALL_PAIRINGS = PAIRINGS_2G + PAIRINGS_1G # get all pairings (for more information on the pairings refer to AllStimuliFiles.xlsx)
    ALL_PAIRINGS = [('gg04','gg11')]#,('gg00', 'gg04')]

    # VARIABLES RELATED TO DYAD FILES
    DURATION = 3 # length of the dyad files
    FPS = 25 # frame rate of the dyad files
    TOTAL_FRMS = DURATION*FPS # total number of frames of the dyad file

    HEIGHT = 1080 # height of the dyad files (in pixel)
    WIDTH = 1920 # width of the dyad files (in pixel)
    HALF_WIDTH = int(WIDTH/2) # half or the dyad files (in pixel)

    AVERAGE_H = 740 # height of the individuals in the first frame (in pixel)
    LOWER_MARGIN = (HEIGHT-AVERAGE_H)/2 # space between the bottom of the dyad file and the feet of the individuals (in pixel)

    AVERAGE_DIST = 700 # distance between the center of mass of both individuals in the first frame (in pixel)
    POS_LEFT = (WIDTH-AVERAGE_DIST)/2 # position of the left actor's center of mass on the x-axis
    POS_RIGHT = WIDTH-POS_LEFT # position of the right actor's center of mass on the x-axis

    # VARIABLES RELATED TO CATCH FILES
    COLOR = (255,0,0,13) # color of the glitch effect

    # create the output folder structure
    create_folder_structure(ROOT_DIRS, SUB_DIRS, SUB_SUB_DIRS)

    # create all combinations for the 1G and 2G pairings
    combinations_HH = create_gesture_combinations(ALL_PAIRINGS,IN_DIR,'HH',GROUP)
    combinations_HR = create_gesture_combinations(ALL_PAIRINGS,IN_DIR,'HR',GROUP)
    all_combinations = combinations_HH + combinations_HR
    all_combs_flat = {item for sublist in all_combinations for item in sublist}

    print(f"Creating image sequences in the directory '{SEQ_DIR}': ")
    for gestures in tqdm(all_combs_flat):
        # determine the interaction and gesture type of the dyad stimuli to be created
        interaction_type = get_interaction_type(gestures[0][IND_ACTOR_START:IND_ACTOR_END],gestures[1][IND_ACTOR_START:IND_ACTOR_END])
        pairing_type = get_pairing_type(gestures[0][IND_GESTURE_START:IND_GESTURE_END],gestures[1][IND_GESTURE_START:IND_GESTURE_END])

        # load the video files of the individual stimuli to be combined into a dyad
        gesture_left = mpy.VideoFileClip(gestures[0],has_mask=True).set_duration(DURATION)
        gesture_right = mpy.VideoFileClip(gestures[1],has_mask=True).fx(mpy.vfx.mirror_x).set_duration(DURATION)

        # calculate the center of gravity of the human body in the resized clip
        center_left = calculate_center(gesture_left)
        center_right = calculate_center(gesture_right)

        # load the background image
        background_transparent = mpy.ImageClip('background_transparent.png',duration=DURATION)

        # create the video composition
        dyad_seq = mpy.CompositeVideoClip([background_transparent,
                                           gesture_left.set_position((POS_LEFT-center_left[0],HEIGHT-gesture_left.size[1]-LOWER_MARGIN)),
                                           gesture_right.set_position((POS_RIGHT-center_right[0],HEIGHT-gesture_right.size[1]-LOWER_MARGIN))
                                           ])

        # Workaround for the moviepy bug that write_videofile() cannot export a video clip with an alpha channel
        img_seq_path = join(SEQ_DIR,pairing_type,interaction_type,f'{GROUP}_DS_l{gestures[0][IND_GESTURE_START:IND_ACTOR_END]}_r{gestures[1][IND_GESTURE_START:IND_ACTOR_END]}')
        mkdir(img_seq_path)
        dyad_seq.write_images_sequence(f'{img_seq_path}/frame%04d.png', FPS, withmask=True, verbose=False, logger=None) # create image sequence of dyad vidoes

    # load the background image
    background_gray = mpy.ImageClip('background_gray.png',duration=DURATION)

    in_dirs = [SEQ_DIR,SEQ_DIR_CATCH_LEFT,SEQ_DIR_CATCH_RIGHT]
    out_dirs = [OUT_DIR,OUT_DIR_CATCH_LEFT,OUT_DIR_CATCH_RIGHT]

    for in_dir, out_dir in zip(in_dirs,out_dirs):
        catch = False
        if in_dir != SEQ_DIR:
            # copy the SEQ_DIR containg all the image sequences of the dyad files
            shutil.copytree(SEQ_DIR, in_dir)
            catch = True

        dir_thresh = 2+len(in_dir)+len(SUB_DIRS[1])+1+len(SUB_SUB_DIRS[0])+1 # length of the longest possible directory name
        subdirs = [subdir for subdir,_,_ in walk(in_dir) if len(subdir) >= dir_thresh] # for all that contain files inside them

        print(f"Creating video files in the directory '{out_dir}': ")
        for subdir in tqdm(subdirs):
            if catch:
                side = in_dir.split('_')[2]
                rand_frm_num = random.randint(5,TOTAL_FRMS-5)
                dyad_name = subdir.split(in_dir,1)[1].replace('DS',f'Catch_{side[0]}{rand_frm_num:04d}')+'.mp4'

                add_glitch_effect(subdir,side,rand_frm_num,COLOR,WIDTH,HALF_WIDTH)
                create_video(subdir,in_dir,out_dir,dir_thresh,background_gray,DURATION,FPS,dyad_name)
            else:
                dyad_name = subdir.split(in_dir,1)[1]+'.mp4'
                create_video(subdir,in_dir,out_dir,dir_thresh,background_gray,DURATION,FPS,dyad_name)

        if catch:
            create_sheet_catchTrials(out_dir, GROUP,TOTAL_FRMS)
        else:
            create_sheet_dyads(out_dir, GROUP)

if __name__ == "__main__":
    main()
