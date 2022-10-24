#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
import re
import random
import openpyxl
import constraint
import shutil
from os import mkdir, makedirs
from os.path import join, dirname, exists

def get_pairing(f):
    # get a unique number that distinguishes the group of a gesture pairing. This group contains all combinations of the
    # two gestures in the 1G, 2G_SAME and 2G_DIFF condition.
    if re.search(r'(gg01|gg18)',f):
        return '0'
    elif re.search(r'(gg04|gg11)',f):
        return '1'
    elif re.search(r'(gg06|gg19)',f):
        return '2'
    elif re.search(r'(gg08|gg20)',f):
        return '3'

def pick_stimuli(all_stimuli, pairing, groups):
    stimuli = []
    for stim in all_stimuli:
        if stim[9] == pairing: # check if the stimulus is from the desired gesture pairing
            # depending on the pairing type, select stimuli with a certain actor pairing in order to minimize repression effects
            if stim[6] == '2G_SAME' and stim[8] == groups[0]:
                stimuli.append(stim)
            if stim[6] == '2G_DIFF' and stim[8] == groups[1]:
                stimuli.append(stim)
            if stim[6] == '1G' and stim[8] == groups[2]:
                stimuli.append(stim)
    return stimuli

def get_stimuli_for_run(all_stimuli, num_of_run, group_allocations):
    stimuli = []
    for key in group_allocations.keys(): # for each unique group of gesture pairings
        # for each pairing type pick stimuli from a actor group that is predfiened in `group_allocations`
        stimuli_pairing = pick_stimuli(all_stimuli,key,group_allocations[key][num_of_run])
        for stim in stimuli_pairing:
            stimuli.append(stim)
    return stimuli

def get_stimuli_for_condition(stimuli_run, condition):
    stimuli_condition = []
    for stim in stimuli_run:
        if f'{stim[6]}_{stim[7]}' == condition: # check if stimuli is from the specified condition (1G, 2G_SAME, 2G_DIFF)
            stimuli_condition.append(stim)
    return stimuli_condition

def generate_possible_run(stimuli_run, conditions_run):
    for stim_pos, cond in enumerate(conditions_run): # iterate over all the conditions for the stimuli that are going to be displayed
        possible_stimuli = get_stimuli_for_condition(stimuli_run,cond) # get a list of possible stimuli for the condition
        rand_ind = random.randrange(len(possible_stimuli))
        stimulus = possible_stimuli[rand_ind] # choose a random stimulus from the list
        conditions_run[stim_pos] = stimulus # replace the condition name with the file that was chosen for the condition
        stimuli_run.remove(stimulus) # remove stimulus from the list of stimuli that are still available for the run

    return conditions_run

def get_avg_dist_group(run):
    avg_dist_group = 0
    groups = ['A','B','C']

    # calculate the avarage distance between stimuli with the same actor group
    for group in groups:
        indices = [i for i, stim in enumerate(run) if stim[8] == group]
        avg_dist_group += sum(indices[cnt+1]-ind for cnt,ind in enumerate(indices[:-1]))/len(run)

    # return a score based on the avarage distance
    return avg_dist_group/len(groups)

def get_avg_dist_gesture(run):
    avg_dist_gesture = 0
    gestures = ['gg01', 'gg18', 'gg04', 'gg11', 'gg06', 'gg19', 'gg08', 'gg20']

    # calculate the avarage distance between stimuli from the same gesture pairing group
    for gesture in gestures:
        indices = [i for i, stim in enumerate(run) if re.search(rf'{gesture}',stim[1])]
        avg_dist_gesture += sum(indices[cnt+1]-ind for cnt,ind in enumerate(indices[:-1]))/len(run)

    # return a score based on the avarage distance
    return avg_dist_gesture/len(gestures)

def get_avg_dist_gesture_by_actor(run):
    avg_dist_gesture_by_actor = 0
    gestures = ['gg01', 'gg18', 'gg04', 'gg11', 'gg06', 'gg19', 'gg08', 'gg20']
    actors = ['f01', 'f02','m02','p']
    gestures_by_actors = [(gesture,actor) for gesture in gestures for actor in actors]

    # calculate the avarage distance between stimuli where the same actor does the same gesture
    for gesture_by_actor in gestures_by_actors:
        indices = [i for i, stim in enumerate(run) if re.search(rf'{gesture_by_actor[0]}_{gesture_by_actor[1]}',stim[1])]
        avg_dist_gesture_by_actor += sum(indices[cnt+1]-ind for cnt,ind in enumerate(indices[:-1]))/len(run)

    # return a score based on the avarage distance
    return avg_dist_gesture_by_actor/len(gestures_by_actors)

def evaluate_run(run):
    # custom objective function to give a rating to each run
    avg_dist_gesture_by_actor = get_avg_dist_gesture_by_actor(run)
    avg_dist_gesture = get_avg_dist_gesture(run)
    avg_dist_group = get_avg_dist_group(run)

    # weighting of the different scores
    score = 0.5*avg_dist_gesture_by_actor+0.25*avg_dist_gesture+0.25*avg_dist_group

    # return final score for the run
    return score

def generate_catch_trials(dyad_stimuli, catch_stimuli, catch_pairings, catch_labels, sides, num_of_run, group_allocations, actor_groups):
    catch_run = []
    catch_pairings_run = catch_pairings[num_of_run*8:num_of_run*8+8] # get pairings for the eight catch files of the run
    labels_run = catch_labels[num_of_run*8:num_of_run*8+8] # get conditions for the eight catch files of this run
    sides_run = sides[num_of_run*8:num_of_run*8+8] # get sides of the catchs for the eight catch files of this run

    for gesture_pairing, label, side in zip(catch_pairings_run, labels_run, sides_run):
        # select catch files corresponding to the actor groups for the different conditions specified for the groups of gesture pairs in this run.
        pairing_group = (get_pairing(''.join(gesture_pairing)))
        actor_group = group_allocations[pairing_group][num_of_run][label]
        # pick a random pairing from the specified actor group
        actor_pairing = random.choice(actor_groups[actor_group])

        for stimuli in catch_stimuli: # select the matching catch file from the list of all catch files
            if re.search(rf'{side}.*{gesture_pairing[0]}_{actor_pairing[0]}.*{gesture_pairing[1]}_{actor_pairing[1]}', stimuli[1]):
                catch_run.append(stimuli)

    return catch_run

def get_best_run(dyad_stimuli, optseq_runs, num_of_run, group_allocations):
    stimuli_run = get_stimuli_for_run(dyad_stimuli, num_of_run, group_allocations)
    conditions_run = [item[1] for item in optseq_runs[num_of_run] if not(item[1] in ['NULL','Catch'])] # get the conditions for this run from the optseq file (omit NULL and Catch)

    best_possible_run = []
    max_score = 0

    for i in range(1,25001): # brutforce over 250000 possible runs and keep the one with the highest score
        possible_run = generate_possible_run(stimuli_run.copy(), conditions_run.copy())
        score = evaluate_run(possible_run)
        if score > max_score:
            max_score = score
            best_possible_run = possible_run
        if i % 25000 == 0:
            print(f'Score after {i} iterations: {max_score} \n')

    return best_possible_run

def main():
    STIM_DIR = '../stimuli'
    EXP_DIR = os.getcwd()

    DAYD_STIMULI = []
    CATCH_STIMULI = []
    OPTSEQ_RUNS = []
    keys = []

    for root, dirs, files in os.walk(STIM_DIR):
        for f in files:
            # extract the information about all dyad files from the excel sheets of the different groups
            if re.search(r'Dyads_..xlsx',f):
                df = pd.read_excel(os.path.join(root,f))
                stimuli_list = df[['FileName','FilePath','GestureCodeLeft','GestureCodeRight','ActorLeft','ActorRight','PairingType','InteractionType','Group']].values.tolist()
                for stimuli in stimuli_list:
                    stimuli.append(get_pairing(stimuli[1]))
                    DAYD_STIMULI.append(tuple(stimuli))
            # extract the information about all catch trials from the excel sheets of the different groups
            if re.search(r'CatchTrials_.*.xlsx',f):
                df = pd.read_excel(os.path.join(root,f))
                catch_list = df[['FileName','FilePath','GestureCodeLeft','GestureCodeRight','ActorLeft','ActorRight','PairingType','InteractionType','Group', 'CatchSide']].values.tolist()
                for catch in catch_list:
                    CATCH_STIMULI.append(tuple(catch))

    for root, dirs, files in os.walk(EXP_DIR):
        for f in files:
            # extract the information about the conditions and the ordering of the presented stimuli from the different optseq2 files
            if f.endswith('.par'):
                key = re.findall(r'\d+',f)
                keys.append(key)
                with open(f,'r') as f:
                    run = [(float(line[:9].strip()), line[-11:].strip(), float(line[17:23])) for line in f.readlines()]
                    OPTSEQ_RUNS.append(run)

    # sort optseq_runs so that the information from the optseq file with the highest score comes first
    OPTSEQ_RUNS = [run for _,run in sorted(zip(keys,OPTSEQ_RUNS))]

    # get all 2G pairings
    PAIRINGS_2G_DIFF = [('gg01','gg18'), ('gg04','gg11'), ('gg06','gg19'), ('gg08','gg20'),
                        ('gg18','gg01'), ('gg11','gg04'), ('gg19','gg06'), ('gg20','gg08')]
    PAIRINGS_2G_SAME = [('gg01','gg01'),('gg04','gg04'),('gg06','gg06'),('gg08','gg08'),
                        ('gg11','gg11'),('gg18','gg18'),('gg19','gg19'),('gg20','gg20')]

    # get all 1G pairings
    PAIRINGS_1G = [('gg00','gg01'), ('gg00','gg04'), ('gg00','gg06'), ('gg00','gg08'),
                   ('gg00','gg11'), ('gg00','gg18'), ('gg00','gg19'), ('gg00','gg20'),
                   ('gg01','gg00'), ('gg04','gg00'), ('gg06','gg00'), ('gg08','gg00'),
                   ('gg11','gg00'), ('gg18','gg00'), ('gg19','gg00'), ('gg20','gg00')]

    # get the different actor groups
    ACTOR_GROUPS = {'A': [('f01', 'f02'),('m02','p'),('f02', 'f01'),('p','m02')],
                    'B': [('f02', 'm02'),('f01','p'),('m02', 'f02'),('p','f01')],
                    'C': [('f01', 'm02'),('f02','p'),('m02', 'f01'),('p','f02')]}

    # Define which actor group to use for which condition in which gesture pairing group.The key indicates the group of
    # gesture pairings. The and the position of the lists within the list stands for the run and position 0 within this
    # list for condition `2G_SAME`, 1 for `2G_DIFF` and 3 for `1G`.
    possible_allocations = [['A','B','C'],['C','A','B'],['B','C','A']]*3
    GROUP_ALLOCATIONS = {}
    for i in range(0,4):
        GROUP_ALLOCATIONS[str(i)] = possible_allocations[0+i:6+i]

    random.seed(61)

    # each of the 32 gesture pairing occurs once, and half of the pairings from each pairing type occur again
    CATCH_PAIRINGS = PAIRINGS_1G + PAIRINGS_2G_DIFF + PAIRINGS_2G_SAME + random.sample(PAIRINGS_2G_DIFF, 4) + random.sample(PAIRINGS_2G_SAME, 4) + random.sample(PAIRINGS_1G, 8)
    # label each pairing with its pairing type (0 for `2G_SAME`, 1 for `2G_DIFF` and 3 for `1G`)
    CATCH_LABELS = [2]*len(PAIRINGS_1G) + [1]*len(PAIRINGS_2G_DIFF) + [0]*len(PAIRINGS_2G_SAME) + [1]*4 + [0]*4 + [2]*8
    # the glitch effect should occur the same amount of time on each side
    SIDES = ['Left', 'Right']*24

    # shuffle the catch pairings and their respective labels
    random.shuffle(SIDES)
    temp = list(zip(CATCH_PAIRINGS, CATCH_LABELS))
    random.shuffle(temp)
    CATCH_PAIRINGS, CATCH_LABELS = zip(*temp)

    dyad_runs = []
    catch_runs = []

    for num_of_run in range(0,6): # for each of the six runs in the experiment
        print(f'Creating catch trials for run number {num_of_run+1}\n')
        catch_run = generate_catch_trials(DAYD_STIMULI, CATCH_STIMULI, CATCH_PAIRINGS, CATCH_LABELS, SIDES, num_of_run, GROUP_ALLOCATIONS, ACTOR_GROUPS) # generate eight catch trials for this run
        catch_runs.append(catch_run)
        print(f'Creating the sequence of stimuli for run number {num_of_run+1}\n')
        dyad_run = get_best_run(DAYD_STIMULI, OPTSEQ_RUNS, num_of_run, GROUP_ALLOCATIONS) # pick the stimuli files used in this run and order them according to the optseq file for the run
        dyad_runs.append(dyad_run)

    # create an excel sheet for each run
    num_of_run = 1
    for dyad_run, optseq_run, catch_run in zip(dyad_runs, OPTSEQ_RUNS, catch_runs):
        df_run = pd.DataFrame(columns=['OnsetTime','Duration','EventName','FileName','FilePath','GestureCodeLeft','GestureCodeRight','ActorLeft','ActorRight','PairingType','InteractionType','Group','CatchSide'])
        dyad_cnt, catch_cnt = 0, 0
        for event in optseq_run:
            event_info = []
            if re.search(r'NULL',event[1]):
                event_info = [event[0], event[2], event[1]]+[np.nan]*10 # add all the information about the NULL event to the dataframe
            elif re.search(r'Catch',event[1]):
                event_info = [event[0], event[2], event[1]]+list(catch_run[catch_cnt]) # add all the information about the catch trial to the dataframe
                catch_cnt += 1
            else:
                event_info = [event[0], event[2], event[1]]+list(dyad_run[dyad_cnt][:-1])+[np.nan] # add all the information about the stimuli to the dataframe
                dyad_cnt += 1
            df_run.loc[len(df_run)] = event_info

        df_run.to_excel(f'Run-{num_of_run:03d}.xlsx', index=False)
        num_of_run += 1

    # Define a constraint satisfaction problem for the possible ordering of the runs within the experiment
    problem = constraint.Problem()

    for i in range(1,7):
        problem.addVariable(str(i),range(1,7))

    # to avoid repression effects the two runs where the same actor group is overrepresented need to be seperated by two other runs
    def run_pairing(run_1, run_2):
        if abs(run_1-run_2) == 3:
            return True

    problem.addConstraint(run_pairing,'14') # in run 1 and 4 actor group A is overrepresented
    problem.addConstraint(run_pairing,'25') # in run 2 and 5 actor group B is overrepresented
    problem.addConstraint(run_pairing,'36') # in run 3 and 6 actor group C is overrepresented
    problem.addConstraint(constraint.AllDifferentConstraint()) # all positions need to be filled with a unique run

    solutions = problem.getSolutions() # get the solution to the CSP (48 solutions)

    col_names = ['Run1','Run2','Run3','Run4','Run5','Run6']
    df_runs = pd.DataFrame(columns=col_names) # create a dataframe containing all possible orderings
    for solution in solutions:
        for key, value in solution.items():
            solution[key] = f'Run-{value:03d}.xlsx' # replace number of the run by the actual name of the excel sheet
        df_runs.loc[len(df_runs)] = dict(sorted(solution.items())).values() # add the sorted solution to the dataframe

    # sort the dataframe after the column names
    df_runs = df_runs.sort_values(by=col_names).reset_index(drop=True)

    # Reorder the dataframe in such a way that each file is position 1 once before the file occurs again in position 1
    indices = []
    chunks = list(range(0,8))

    random.shuffle(chunks)

    for i in chunks:
        for ind in [i,i+16,i+32,i+8,i+24,i+40]:
            indices.append(ind)

    df_runs = df_runs.reindex(indices).reset_index(drop=True)

    # write the dataframe to an excel sheet
    df_runs.to_excel(f'ExperimentOrder.xlsx', index=False)

    # get the filepaths of all the different dyad and catch files used in the different runs
    all_files = []
    for num_of_run in range(1,7):
        file_paths = pd.read_excel(f'Run-{num_of_run:03d}.xlsx', usecols='E').dropna().values.tolist()
        for file_path in file_paths:
            all_files.append(file_path)

    # only keep the unique files
    all_unique_files = {file_path for sublist in all_files for file_path in sublist}

    # create a new directory that only contains the files that are actually used in the experimenz
    for src in all_unique_files:
        dst = join(EXP_DIR, src)
        dstfolder = dirname(dst)
        if not exists(dstfolder):
            makedirs(dstfolder)
        stim = join(STIM_DIR, src)
        shutil.copy(stim,dst)

if __name__ == "__main__":
    main()
