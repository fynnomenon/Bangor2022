#!/usr/bin/env python
# coding: utf-8

# import necessary packages
import moviepy.editor as mpy
import subprocess
import numpy as np
import cv2
from tqdm.auto import tqdm
from tqdm.contrib import tzip
from os import mkdir, listdir
from os.path import join

def remove_outliers(src):
    num_labels,labels,stats,centroids = cv2.connectedComponentsWithStats(src,connectivity=4,ltype=None)
    img = np.zeros((src.shape[0],src.shape[1]),np.uint8) # create a black background of all 0
    for i in range(1,num_labels):
        mask = labels == i # this step is to determine the location of the area through labels, assign labels information to the mask array, and then use the mask array as the index of img array
        if stats[i][4] > 100:
            img[mask] = 255 # areas larger than 100 shall be painted white, and areas smaller than 100 shall be painted black
        else:
            img[mask] = 0
    return img

def get_contours(frm):
    # convert frame to grayscale
    frm_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
    # remove tiny particels
    frm_out = remove_outliers(frm_gray)
    # convert frame to black and white
    frm_thresh = cv2.threshold(frm_out,0,255,cv2.THRESH_BINARY)[1]
    # extract contours
    contours,_ = cv2.findContours(frm_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    return contours

def get_bbox_coords(clip, t=0):
    x_bbox=y_bbox=w_bbox=h_bbox=0
    # get the frame
    frm = clip.get_frame(t)
    # get the bounding box of the frame
    contours = get_contours(frm)
    # get the coordinates of the bounding box
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w > 100 and h > 100: # only consider rectangles of relevant size
            x_bbox,y_bbox,w_bbox,h_bbox=x,y,w,h

    return x_bbox,y_bbox,w_bbox,h_bbox

def crop_and_resize(clip):
    clip_x, clip_y = clip.size
    bbox = [clip_x,0,clip_y,0]
    average_h = 740

    # iterate through frames of the video clip
    for frm in clip.iter_frames():
        contours = get_contours(frm)

        # iterate over contours
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            # save rectangle that contains all boundingboxes inside it
            if x < bbox[0]:
                bbox[0] = x
            if x+w > bbox[1]:
                bbox[1] = x+w
            if y < bbox[2]:
                bbox[2] = y
            if y+h > bbox[3]:
                bbox[3] = y+h

    # crop and resize the clip
    _,_,_,clip_h = get_bbox_coords(clip)
    scaling_factor =  average_h/clip_h

    cropped_clip = clip.fx(mpy.vfx.crop, x1=bbox[0],x2=bbox[1],y1=bbox[2],y2=bbox[3])
    resized_clip = cropped_clip.resize(scaling_factor)

    return resized_clip

def fix_rotation(clip):
    # Workaround for the moviepy bug causing videos with rotation metadata to be stretched
    if clip.rotation in (90,270):
            clip = clip.resize(clip.size[::-1])
            clip.rotation = 0

    return clip

def main():
    # get a list of all files in the input directory
    in_dir = 'IndividualStimuliCutted'
    file_names = listdir(in_dir)
    file_paths = [join(in_dir, f) for f in file_names]

    out_dir = 'IndividualStimuliCleaned'
    mkdir(out_dir)

    seq_dir = 'ImageSequencesIndividuals'
    mkdir(seq_dir)

    for f_name,f_path in tzip(file_names,file_paths):
        # load the video files of the individual stimuli to be cleaned
        clip = mpy.VideoFileClip(f_path, has_mask=True)
        # Workaround for the moviepy bug causing videos with rotation metadata to be stretched
        temp_clip = fix_rotation(clip)
        # transform the individual stimuli files
        cleaned_clip = crop_and_resize(temp_clip)
        # make the video grayscale
        grayscale_clip = cleaned_clip.fx(mpy.vfx.blackwhite)

        # Workaround for the moviepy bug that write_videofile() cannot export a video clip with an alpha channel
        img_seq_path = join(seq_dir, f_name[:-4])
        mkdir(img_seq_path)
        fps = grayscale_clip.fps
        grayscale_clip.write_images_sequence(f'{img_seq_path}/frame%04d.png', fps=fps, withmask=True, verbose=False, logger=None) # create image sequence of cleaned video

        command = f'ffmpeg -i {img_seq_path}/frame%4d.png -framerate {fps} -pix_fmt yuva444p10le -vcodec prores_ks -threads 6 {out_dir}/{f_name}' # create transparent video out of image sequence
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
