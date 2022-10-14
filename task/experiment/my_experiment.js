/********************** 
 * My_Experiment Test *
 **********************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2022.2.3.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'my_experiment';  // from the Builder filename that created this script
let expInfo = {
    'id': '',
    'session': '',
    'run': '',
};

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([1.0, (- 1.0), (- 1.0)]),
  units: 'norm',
  waitBlanking: true
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(waitingRoutineBegin());
flowScheduler.add(waitingRoutineEachFrame());
flowScheduler.add(waitingRoutineEnd());
flowScheduler.add(fixation_beginningRoutineBegin());
flowScheduler.add(fixation_beginningRoutineEachFrame());
flowScheduler.add(fixation_beginningRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);
flowScheduler.add(fixation_endRoutineBegin());
flowScheduler.add(fixation_endRoutineEachFrame());
flowScheduler.add(fixation_endRoutineEnd());
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.EXP);


var currentLoop;
var frameDur;
async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2022.2.3';
  expInfo['OS'] = window.navigator.platform;

  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["id"]}_${expInfo["session"]}_${expInfo["run"]}_${expName}_${expInfo["date"]}`);

  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  
  return Scheduler.Event.NEXT;
}


var waitingClock;
var waiting_txt;
var trigger;
var fixation_beginningClock;
var fixation_cross_beginning;
var mainClock;
var key_resp;
var fixation_cross;
var fixation_endClock;
var fixation_cross_end;
var globalClock;
var routineTimer;
async function experimentInit() {
  // Initialize components for Routine "waiting"
  waitingClock = new util.Clock();
  waiting_txt = new visual.TextStim({
    win: psychoJS.window,
    name: 'waiting_txt',
    text: 'Preloading done! Waiting for trigger...',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], height: 0.08,  wrapWidth: 1.4, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('black'),  opacity: 1.0,
    depth: -1.0 
  });
  
  trigger = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "fixation_beginning"
  fixation_beginningClock = new util.Clock();
  fixation_cross_beginning = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation_cross_beginning', units : 'pix', 
    vertices: 'cross', size:[100, 100],
    ori: 0.0, pos: [0, 0],
    lineWidth: 0.4, 
    colorSpace: 'rgb',
    lineColor: new util.Color([0.0, 0.0, 0.0]),
    fillColor: new util.Color('white'),
    opacity: undefined, depth: -1, interpolate: true,
  });
  
  // Initialize components for Routine "main"
  mainClock = new util.Clock();
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  fixation_cross = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation_cross', units : 'pix', 
    vertices: 'cross', size:[100, 100],
    ori: 0.0, pos: [0, 0],
    lineWidth: 0.4, 
    colorSpace: 'rgb',
    lineColor: new util.Color([0.0, 0.0, 0.0]),
    fillColor: new util.Color('white'),
    opacity: undefined, depth: -2, interpolate: true,
  });
  
  // Initialize components for Routine "fixation_end"
  fixation_endClock = new util.Clock();
  fixation_cross_end = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation_cross_end', units : 'pix', 
    vertices: 'cross', size:[100, 100],
    ori: 0.0, pos: [0, 0],
    lineWidth: 0.4, 
    colorSpace: 'rgb',
    lineColor: new util.Color([0.0, 0.0, 0.0]),
    fillColor: new util.Color('white'),
    opacity: undefined, depth: 0, interpolate: true,
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}


var t;
var frameN;
var continueRoutine;
var _trigger_allKeys;
var waitingComponents;
function waitingRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'waiting' ---
    t = 0;
    waitingClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    trigger.keys = undefined;
    trigger.rt = undefined;
    _trigger_allKeys = [];
    // keep track of which components have finished
    waitingComponents = [];
    waitingComponents.push(waiting_txt);
    waitingComponents.push(trigger);
    
    for (const thisComponent of waitingComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function waitingRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'waiting' ---
    // get current time
    t = waitingClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *waiting_txt* updates
    if (((preloading == False)) && waiting_txt.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      waiting_txt.tStart = t;  // (not accounting for frame time here)
      waiting_txt.frameNStart = frameN;  // exact frame index
      
      waiting_txt.setAutoDraw(true);
    }

    
    // *trigger* updates
    if (((preloading == False)) && trigger.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      trigger.tStart = t;  // (not accounting for frame time here)
      trigger.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      trigger.clock.reset();
      trigger.start();
      trigger.clearEvents();
    }

    if (trigger.status === PsychoJS.Status.STARTED) {
      let theseKeys = trigger.getKeys({keyList: ['t'], waitRelease: false});
      _trigger_allKeys = _trigger_allKeys.concat(theseKeys);
      if (_trigger_allKeys.length > 0) {
        trigger.keys = _trigger_allKeys[_trigger_allKeys.length - 1].name;  // just the last key pressed
        trigger.rt = _trigger_allKeys[_trigger_allKeys.length - 1].rt;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of waitingComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function waitingRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'waiting' ---
    for (const thisComponent of waitingComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(trigger.corr, level);
    }
    psychoJS.experiment.addData('trigger.keys', trigger.keys);
    if (typeof trigger.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('trigger.rt', trigger.rt);
        routineTimer.reset();
        }
    
    trigger.stop();
    // the Routine "waiting" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var fixation_beginningComponents;
function fixation_beginningRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'fixation_beginning' ---
    t = 0;
    fixation_beginningClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    routineTimer.add(8.000000);
    // update component parameters for each repeat
    // Run 'Begin Routine' code from code_2
    /* Syntax Error: Fix Python code */
    // keep track of which components have finished
    fixation_beginningComponents = [];
    fixation_beginningComponents.push(fixation_cross_beginning);
    
    for (const thisComponent of fixation_beginningComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


var frameRemains;
function fixation_beginningRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'fixation_beginning' ---
    // get current time
    t = fixation_beginningClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fixation_cross_beginning* updates
    if (t >= 0.0 && fixation_cross_beginning.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation_cross_beginning.tStart = t;  // (not accounting for frame time here)
      fixation_cross_beginning.frameNStart = frameN;  // exact frame index
      
      fixation_cross_beginning.setAutoDraw(true);
    }

    frameRemains = 0.0 + 8.0 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (fixation_cross_beginning.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fixation_cross_beginning.setAutoDraw(false);
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of fixation_beginningComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function fixation_beginningRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'fixation_beginning' ---
    for (const thisComponent of fixation_beginningComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var trials;
function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: run_file,
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(mainRoutineBegin(snapshot));
      trialsLoopScheduler.add(mainRoutineEachFrame());
      trialsLoopScheduler.add(mainRoutineEnd(snapshot));
      trialsLoopScheduler.add(trialsLoopEndIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}


async function trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}


function trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}


var _key_resp_allKeys;
var mainComponents;
function mainRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'main' ---
    t = 0;
    mainClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    // update component parameters for each repeat
    key_resp.keys = undefined;
    key_resp.rt = undefined;
    _key_resp_allKeys = [];
    // keep track of which components have finished
    mainComponents = [];
    mainComponents.push(key_resp);
    mainComponents.push(fixation_cross);
    
    for (const thisComponent of mainComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function mainRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'main' ---
    // get current time
    t = mainClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *key_resp* updates
    if (t >= 0 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp.tStart = t;  // (not accounting for frame time here)
      key_resp.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      key_resp.clock.reset();
      key_resp.start();
      key_resp.clearEvents();
    }

    frameRemains = 0 + Duration - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (key_resp.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      key_resp.status = PsychoJS.Status.FINISHED;
  }

    if (key_resp.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp.getKeys({keyList: ['r', 'b', 'g', 'y'], waitRelease: false});
      _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
      if (_key_resp_allKeys.length > 0) {
        key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
        key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
      }
    }
    
    
    // *fixation_cross* updates
    if (((play == 'NULL')) && fixation_cross.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation_cross.tStart = t;  // (not accounting for frame time here)
      fixation_cross.frameNStart = frameN;  // exact frame index
      
      fixation_cross.setAutoDraw(true);
    }

    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of mainComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function mainRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'main' ---
    for (const thisComponent of mainComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp.corr, level);
    }
    psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
    if (typeof key_resp.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
        }
    
    key_resp.stop();
    // the Routine "main" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


var fixation_endComponents;
function fixation_endRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'fixation_end' ---
    t = 0;
    fixation_endClock.reset(); // clock
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    routineTimer.add(16.000000);
    // update component parameters for each repeat
    // keep track of which components have finished
    fixation_endComponents = [];
    fixation_endComponents.push(fixation_cross_end);
    
    for (const thisComponent of fixation_endComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}


function fixation_endRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'fixation_end' ---
    // get current time
    t = fixation_endClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *fixation_cross_end* updates
    if (t >= 0.0 && fixation_cross_end.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      fixation_cross_end.tStart = t;  // (not accounting for frame time here)
      fixation_cross_end.frameNStart = frameN;  // exact frame index
      
      fixation_cross_end.setAutoDraw(true);
    }

    frameRemains = 0.0 + 16.0 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
    if (fixation_cross_end.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      fixation_cross_end.setAutoDraw(false);
    }
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of fixation_endComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}


function fixation_endRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'fixation_end' ---
    for (const thisComponent of fixation_endComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}


function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  
  
  
  
  
  
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});
  
  return Scheduler.Event.QUIT;
}
