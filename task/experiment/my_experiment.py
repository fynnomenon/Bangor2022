#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.3),
    on October 24, 2022, at 14:50
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

import psychopy
psychopy.useVersion('latest')


# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code
# start an individual clock
globalClock = core.Clock()


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.3'
expName = 'my_experiment'  # from the Builder filename that created this script
expInfo = {
    'id': '',
    'session': '',
    'run': '',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + f"data/{expInfo['id']}_{expInfo['session']}_{expInfo['run']}_{expName}_{expInfo['date']}"

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\fynna\\OneDrive\\Dokumente\\Bangor\\psychopy\\my_experiment\\my_experiment.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='Monitor', color=[-0.1765, -0.1765, -0.1765], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='norm')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "waiting" ---
# Run 'Begin Experiment' code from code
import pandas as pd

# read in the run orders for all different sessions
ordering_file = pd.read_excel('ExperimentOrder.xlsx')
# get the order for the specified session (1-48)
run_files = ordering_file.iloc[int(expInfo['session'])-1].to_list()
# get the run file for the specified run (1-6)
run_file = run_files[int(expInfo['run'])-1]

# save the file paths of the videos that are displayed in this run in a list
file_paths = []
# get the file paths from the excel sheet and drop the rows with a NULL vent
paths = pd.read_excel(run_file, usecols='E').dropna().values.tolist()
for path in paths:
    file_paths.append(path)
# flatten the list and only keep unique elements
file_paths = {path for sublist in file_paths for path in sublist}
waiting_txt = visual.TextStim(win=win, name='waiting_txt',
    text='Preloading done! Waiting for trigger...',
    font='Arial',
    pos=(0, 0), height=0.08, wrapWidth=1.4, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-1.0);
trigger = keyboard.Keyboard()

# --- Initialize components for Routine "fixation_beginning" ---
fixation_cross_beginning = visual.ShapeStim(
    win=win, name='fixation_cross_beginning', vertices='cross',units='pix', 
    size=(100, 100),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.4,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)

# --- Initialize components for Routine "main" ---
key_resp = keyboard.Keyboard()
fixation_cross = visual.ShapeStim(
    win=win, name='fixation_cross', vertices='cross',units='pix', 
    size=(100,100),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.4,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)

# --- Initialize components for Routine "fixation_end" ---
fixation_cross_end = visual.ShapeStim(
    win=win, name='fixation_cross_end', vertices='cross',units='pix', 
    size=(100, 100),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.4,     colorSpace='rgb',  lineColor=[0.0000, 0.0000, 0.0000], fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "waiting" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code
import pandas as pd

# start preloading the videos
preloading = True

stimuli = {}
for path in file_paths:
    # load the video (in a smaller size to make the prelaoding a bit faster) from 
    # the path specified before as a MovieStim3 object and append it to a stimuli 
    # directory with the file path as the key. 
    stimuli[path] = visual.MovieStim3(win=win,filename=path, name=path[:-4], size=(1760,990))

preloading = False

# Note: After extensive testing, I have come to the conclusion that the 
# MovieStims are considered static elements now and are therefore loaded before 
# the experiment starts, no matter where you place the preloading code. 
# Therefore, it is also not possible to display a corresponding text during the 
# preloading. 
trigger.keys = []
trigger.rt = []
_trigger_allKeys = []
# keep track of which components have finished
waitingComponents = [waiting_txt, trigger]
for thisComponent in waitingComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "waiting" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *waiting_txt* updates
    if waiting_txt.status == NOT_STARTED and preloading == False:
        # keep track of start time/frame for later
        waiting_txt.frameNStart = frameN  # exact frame index
        waiting_txt.tStart = t  # local t and not account for scr refresh
        waiting_txt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(waiting_txt, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'waiting_txt.started')
        waiting_txt.setAutoDraw(True)
    
    # *trigger* updates
    if trigger.status == NOT_STARTED and preloading == False:
        # keep track of start time/frame for later
        trigger.frameNStart = frameN  # exact frame index
        trigger.tStart = t  # local t and not account for scr refresh
        trigger.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(trigger, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.addData('trigger.started', t)
        trigger.status = STARTED
        # keyboard checking is just starting
        trigger.clock.reset()  # now t=0
        trigger.clearEvents(eventType='keyboard')
    if trigger.status == STARTED:
        theseKeys = trigger.getKeys(keyList=['t'], waitRelease=False)
        _trigger_allKeys.extend(theseKeys)
        if len(_trigger_allKeys):
            trigger.keys = _trigger_allKeys[-1].name  # just the last key pressed
            trigger.rt = _trigger_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in waitingComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "waiting" ---
for thisComponent in waitingComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if trigger.keys in ['', [], None]:  # No response was made
    trigger.keys = None
thisExp.addData('trigger.keys',trigger.keys)
if trigger.keys != None:  # we had a response
    thisExp.addData('trigger.rt', trigger.rt)
thisExp.nextEntry()
# the Routine "waiting" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "fixation_beginning" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from code_2
# declare all variables that are used afterwards and set them to their default value
play = ''
key_pressed = 0
conditions = ['Start']
# keep track of which components have finished
fixation_beginningComponents = [fixation_cross_beginning]
for thisComponent in fixation_beginningComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation_beginning" ---
while continueRoutine and routineTimer.getTime() < 8.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fixation_cross_beginning* updates
    if fixation_cross_beginning.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        fixation_cross_beginning.frameNStart = frameN  # exact frame index
        fixation_cross_beginning.tStart = t  # local t and not account for scr refresh
        fixation_cross_beginning.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(fixation_cross_beginning, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'fixation_cross_beginning.started')
        fixation_cross_beginning.setAutoDraw(True)
    if fixation_cross_beginning.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > fixation_cross_beginning.tStartRefresh + 8.0-frameTolerance:
            # keep track of stop time/frame for later
            fixation_cross_beginning.tStop = t  # not accounting for scr refresh
            fixation_cross_beginning.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_cross_beginning.stopped')
            fixation_cross_beginning.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixation_beginningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation_beginning" ---
for thisComponent in fixation_beginningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from code_2
# save the time at which the trials start
start_trials = globalClock.getTime()


# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-8.000000)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(run_file),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "main" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_3
    # save the time at which the current trial started
    start_trial = globalClock.getTime()
    # append the name of the current event to the conditions list
    conditions.append(EventName)
    
    
    if conditions[-1] == 'NULL':
        play = 'NULL'
    else:
        # if the current condition is a catch trial or a stimuli get its MovieStim3
        # object from the stimuli dictionary. Use FilePath as a key.
        stim = stimuli[FilePath]
        # set the MovieStim3 object to PLAYING
        stim.play()
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    mainComponents = [key_resp, fixation_cross]
    for thisComponent in mainComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "main" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_3
        import numpy as np
        
        if conditions[-1] != 'NULL': # if the current condition is a catch trial or a stimuli
            if key_resp.keys in ('r','b', 'g', 'y'): # save if there was a button press
                key_pressed = 1
            # if the trial is longer than the video duration (due to frame dropping), pause
            # the video and display the last frame until the routine ends
            if np.ceil(t) == stim.duration:
                stim.pause()
            # draw the video frame
            stim.draw()
        # if the length of the routine is longer than or equal to the planned duration, 
        # stop the routine (use Duration -0.01 to account for minor timing issues)
        if t >= Duration - 0.01: 
            continueRoutine = False
        
        # *key_resp* updates
        if key_resp.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            key_resp.status = STARTED
            # keyboard checking is just starting
            key_resp.clock.reset()  # now t=0
            key_resp.clearEvents(eventType='keyboard')
        if key_resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > key_resp.tStartRefresh + Duration-frameTolerance:
                # keep track of stop time/frame for later
                key_resp.tStop = t  # not accounting for scr refresh
                key_resp.frameNStop = frameN  # exact frame index
                key_resp.status = FINISHED
        if key_resp.status == STARTED:
            theseKeys = key_resp.getKeys(keyList=['r','b', 'g', 'y'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
        
        # *fixation_cross* updates
        if fixation_cross.status == NOT_STARTED and play == 'NULL':
            # keep track of start time/frame for later
            fixation_cross.frameNStart = frameN  # exact frame index
            fixation_cross.tStart = t  # local t and not account for scr refresh
            fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_cross, 'tStartRefresh')  # time at next scr refresh
            fixation_cross.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mainComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "main" ---
    for thisComponent in mainComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_3
    # save the key responses and their properties to the data file
    if key_pressed == 1 and 'Catch' in conditions[-2:]:
        thisExp.addData('key_resp', 'got catch')
    elif key_pressed == 0 and 'Catch' in conditions[-2:]:
        thisExp.addData('key_resp', 'missed catch')
    elif key_pressed == 1:
        thisExp.addData('key_resp', 'false press')
    else:
        thisExp.addData('key_resp', 'no press')
    
    # save the on and offset times of the trials to the data file
    thisExp.addData('AbsoluteOnsetTime', start_trial)
    thisExp.addData('RelativeOnsetTime', start_trial - start_trials)
    end_trial = globalClock.getTime()
    thisExp.addData('AbsoluteOffsetTime', end_trial)
    thisExp.addData('RelativeOffsetTime', end_trial - start_trials)
    thisExp.addData('ActualDuration', end_trial - start_trial)
    
    # set the variables to their default value for the next trial
    play = ''
    key_pressed = 0
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    trials.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        trials.addData('key_resp.rt', key_resp.rt)
    # the Routine "main" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'trials'

# get names of stimulus parameters
if trials.trialList in ([], [None], None):
    params = []
else:
    params = trials.trialList[0].keys()
# save data for this loop
trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# --- Prepare to start Routine "fixation_end" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
fixation_endComponents = [fixation_cross_end]
for thisComponent in fixation_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation_end" ---
while continueRoutine and routineTimer.getTime() < 16.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fixation_cross_end* updates
    if fixation_cross_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        fixation_cross_end.frameNStart = frameN  # exact frame index
        fixation_cross_end.tStart = t  # local t and not account for scr refresh
        fixation_cross_end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(fixation_cross_end, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'fixation_cross_end.started')
        fixation_cross_end.setAutoDraw(True)
    if fixation_cross_end.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > fixation_cross_end.tStartRefresh + 16.0-frameTolerance:
            # keep track of stop time/frame for later
            fixation_cross_end.tStop = t  # not accounting for scr refresh
            fixation_cross_end.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_cross_end.stopped')
            fixation_cross_end.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixation_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation_end" ---
for thisComponent in fixation_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-16.000000)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
