#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '1.0.0 (20180710)'
__maintainer__ = 'Shi YU'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'

import sys
import random
import pygame
from moviepy.editor import *
import datetime
import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyaxb as psypsyaxb
import libpsypsy.psypsyinterface as psypsyinterface
import libpsypsy.psypsyvideo as psypsyvideo
import re


def write_result_phase3(output, subj, start_time, condition_p3, trial_number, trial_on, trial_off,
                        end, duration, trial_type, stimulus, log):
    f = open(output, 'a')
    result_list = [subj, start_time, condition_p3, trial_number, str(trial_on), str(trial_off),
                   end, str(duration), trial_type, stimulus, log]
    result = "\t".join(result_list)
    print(result, file=f)
    f.close()


# Phase 3 Habituation ===================================================
def habituation_3(subj, condition_p3, skip_to_3, path, screen, screen_width, screen_height):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time
    background_black = (0, 0, 0)  # black
    background_white = (255, 255, 255)  # white
    psypsyinterface.clear_screen(screen, background_black)
    # Path to files ==========================================================
    # path to experiment materials
    phase3_path = path["path"] + path["phase3"]

    # Video Path
    video_path = phase3_path + "final_media/"

    attention_video = "attention.mov"
    pretest_video = "pretest.mov"

    attention_getter = video_path + attention_video
    pretest = video_path + pretest_video
    posttest_video = video_path + "pretest.mov"

    hab_video_path = phase3_path + "hab_test/"

    # Stimuli Path
    stimuli_file = "exp1_p3_test_trial.csv"

    # output
    output = "./results/exp1_p3_results.csv"

    # Check experiment condition ==============================================
    u = "u"
    y = "y"

    if skip_to_3:
        u = "a"
        y = "i"

    if condition_p3 == "u-c":
        habituation = u
    elif condition_p3 == "u-s":
        habituation = u
    elif condition_p3 == "y-c":
        habituation = y
    elif condition_p3 == "y-s":
        habituation = y
    else:
        raise ValueError('something is wrong in condition')

    # Start Experiment =======================================================
    # Attention-getter ==================================
    # loop video until there's a key press
    trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    trial_start = pygame.time.get_ticks()

    psypsyvideo.play_video_loop(attention_getter, screen, -1)

    trial_end = pygame.time.get_ticks()
    duration = trial_end - trial_start
    trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    write_result_phase3(output, subj, start_time, condition_p3, "1", trial_on, trial_off,
                        "keypress", duration, "attention-getter", "attention.mov", "NA")

    psypsyinterface.clear_screen(screen, background_black)

    # pretest ===========================================
    # loop video until there's a key press
    trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    trial_start = pygame.time.get_ticks()

    # psypsyvideo.play_video_loop(pretest, screen, -1)
    prestest_video = VideoFileClip(pretest)
    key = psypsyvideo.play_video_2s(prestest_video, screen)

    trial_end = pygame.time.get_ticks()
    duration = trial_end - trial_start
    trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    write_result_phase3(output, subj, start_time, condition_p3, "2", trial_on, trial_off,
                        key, duration, "pretest", "prestest.mov", "NA")

    psypsyinterface.clear_screen(screen, background_black)

    # Habituation section ====================================================
    # ========================================================================
    # # Attention-getter ==================================
    # # loop video until there's a key press
    # trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    # trial_start = pygame.time.get_ticks()
    #
    # attention = VideoFileClip(attention_getter)
    # stop = False
    # while not stop:
    #     stop = psypsyvideo.play_video(attention, screen)
    #
    # trial_end = pygame.time.get_ticks()
    # duration = trial_end - trial_start
    # trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    # write_result_phase3(output, subj, start_time, condition_p3, "3", trial_on, trial_off,
    #                     "keypress", duration, "attention-getter", "attention.mov", "NA")

    trial_duration_list = []
    hab_i = 1
    while hab_i < 25:  # reach 24 habituation trial

        # Attention-getter ==================================
        # loop video until there's a key press
        trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        trial_start = pygame.time.get_ticks()

        psypsyvideo.play_video_loop(attention_getter, screen, -1)

        trial_end = pygame.time.get_ticks()
        duration = trial_end - trial_start
        trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

        write_result_phase3(output, subj, start_time, condition_p3, str(hab_i + 2), trial_on, trial_off,
                            "keypress", duration, "attention-getter", "attention.mov", "NA")

        psypsyinterface.clear_screen(screen, background_black)

        trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        trial_start = pygame.time.get_ticks()
        # Load habituation video depends on the condition
        habituation_file = "hab-" + habituation + "_trial.mp4"
        habituation_trial_video = hab_video_path + "hab-" + habituation + "_trial.mp4"
        clip_habituation = VideoFileClip(habituation_trial_video)

        # Habituation trial
        # Trial ends when the movie finishes, or when there's no key press for the last 2 seconds
        key = psypsyvideo.play_video_2s(clip_habituation, screen)

        trial_end = pygame.time.get_ticks()
        duration = trial_end - trial_start
        trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

        log = "NA"

        trial_duration_list.append(duration)

        # Calculate average duration
        if len(trial_duration_list) > 3:
            order = trial_duration_list[:]
            ordered = sorted(order)
            average_duration_long = int((ordered[-1] + ordered[-2] + ordered[-3]) / 3)
            last_three_duration = int((trial_duration_list[-1] + trial_duration_list[-2] + trial_duration_list[-3]) / 3)
            log = str(average_duration_long) + " / " + str(last_three_duration)
            if last_three_duration < (average_duration_long * 0.6):
                log = str(average_duration_long) + " / " + str(last_three_duration) + "_criterion_met"
                write_result_phase3(output, subj, start_time, condition_p3, str(hab_i + 2), trial_on, trial_off,
                                    key, duration, "habituation", habituation_file, log)
                break

        if hab_i == 24:
            write_result_phase3(output, subj, start_time, condition_p3, str(hab_i + 2), trial_on, trial_off,
                                key, duration, "habituation", habituation_file, log + "_24_trial")
        else:
            write_result_phase3(output, subj, start_time, condition_p3, str(hab_i + 2), trial_on, trial_off,
                                key, duration, "habituation", habituation_file, log)

        hab_i += 1

        psypsyinterface.clear_screen(screen, background_black)

    # Test section ===========================================================
    # ========================================================================
    # # attention getter
    # # loop video until there's a key press
    # trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    # trial_start = pygame.time.get_ticks()
    #
    # psypsyvideo.play_video_loop(attention_getter, screen, -1)
    #
    # trial_end = pygame.time.get_ticks()
    # duration = trial_end - trial_start
    # trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    #
    # write_result_phase3(output, subj, start_time, condition_p3, str(hab_i + 3), trial_on, trial_off,
    #                     "keypress", duration, "attention-getter", "attention.mov", "NA")
    #
    # psypsyinterface.clear_screen(screen, background_black)

    # Test trial =======================================================================
    trial, header_index = psypsyio.read_stimuli(stimuli_file, "\t")

    index = 0
    for i in range(trial["trial_number"]):
        screen.fill(background_black)
        pygame.display.flip()
        # Attention-getter ==================================
        # loop video until there's a key press
        trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        trial_start = pygame.time.get_ticks()

        psypsyvideo.play_video_loop(attention_getter, screen, -1)

        trial_end = pygame.time.get_ticks()
        duration = trial_end - trial_start
        trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

        write_result_phase3(output, subj, start_time, condition_p3, str(i + hab_i + 3), trial_on, trial_off,
                            "keypress", duration, "attention-getter", "attention.mov", "NA")

        psypsyinterface.clear_screen(screen, background_black)

        trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        trial_start = pygame.time.get_ticks()

        # replace file name to correspond to conditions
        trial_video_file = trial[condition_p3][i]
        if skip_to_3:
            trial_video_file = re.sub(r"u", "a", trial_video_file)
            trial_video_file = re.sub(r"y", "i", trial_video_file)

        video_file = hab_video_path + "test-" + trial_video_file + "_trial" + ".mp4"

        # Each trial ends when the sound file finishes, or when there's a key press
        test_video = VideoFileClip(video_file)
        key = psypsyvideo.play_video_2s(test_video, screen)

        trial_end = pygame.time.get_ticks()
        duration = trial_end - trial_start
        trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        write_result_phase3(output, subj, start_time, condition_p3, str(i + hab_i + 3), trial_on, trial_off,
                            key, duration, "test", trial_video_file, "NA")

        index = i + hab_i + 4

        psypsyinterface.clear_screen(screen, background_black)

    # Loop attention-getter
    trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    trial_start = pygame.time.get_ticks()

    psypsyvideo.play_video_loop(attention_getter, screen, -1)

    trial_end = pygame.time.get_ticks()
    duration = trial_end - trial_start
    trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    write_result_phase3(output, subj, start_time, condition_p3, str(index), trial_on, trial_off,
                        "keypress", duration, "attention-getter", "attention.mov", "NA")

    psypsyinterface.clear_screen(screen, background_black)

    # Loop video posttest.mov
    trial_on = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    trial_start = pygame.time.get_ticks()

    # psypsyvideo.play_video_loop(posttest_video, screen, -1)
    prestest_video = VideoFileClip(pretest)
    key = psypsyvideo.play_video_2s(prestest_video, screen)

    trial_end = pygame.time.get_ticks()
    duration = trial_end - trial_start
    trial_off = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    write_result_phase3(output, subj, start_time, condition_p3, str(index + 1), trial_on, trial_off,
                        key, duration, "posttest", "pretest.mov", "NA")

    psypsyinterface.clear_screen(screen, background_black)
    pygame.quit()


if __name__ == "__main__":
    # sys.argv
    participant_id = sys.argv[1]
    skip_to_3 = False

    condition_list_p3 = ["u-c", "u-s", "y-c", "y-s"]
    condition_p3 = random.choice(condition_list_p3)

    background_black = (0, 0, 0)  # black
    # Initialisation Pygame
    screen, screen_width, screen_height = psypsyinterface.initialisation_pygame(background_black)

    path = {
        "path": "Exp_1_looking_time/",
        # Phase 1
        "phase1": "2018tsi_audiovisual/",
        # Phase 2
        "phase2": "2018tsi_lex/",
        # Phase 3
        "phase3": "2018tsi_nn/"
    }

    habituation_3(participant_id, condition_p3, skip_to_3, path, screen, screen_width, screen_height)

