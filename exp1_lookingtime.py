#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '1.0.0 (20180710)'
__maintainer__ = 'Shi YU'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'

# ============================================
#                                            =
# Looking-time infant study                  =
#                                            =
# ============================================

import sys
import random
import re
import pygame
from moviepy.editor import *
import datetime
import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyaxb as psypsyaxb
import libpsypsy.psypsyinterface as psypsyinterface
import libpsypsy.psypsyvideo as psypsyvideo


def write_result_phase1(output, subj, start_time, condition_p1, trial_number, trial_time, trial_type,
                        trial_video_l, trial_video_r, trial_sound):
    f = open(output, 'a')
    result_list = [subj, start_time, condition_p1, trial_number, trial_time, trial_type,
                   trial_video_l, trial_video_r, trial_sound]
    result = "\t".join(result_list)
    print(result, file=f)
    f.close()


# Phase 1 AV matching ============================================
def av_matching_1(subj, condition_p1, path, screen):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time
    # Path to files =================================================================================
    # path to experiment materials
    phase1_path = path["path"] + path["phase1"] + "infants/"

    # path to video files
    video_path = phase1_path
    # path to sound files
    sound_path = phase1_path

    # path to attention-getter
    video_attention_getter = phase1_path + "attention.mov"

    # Visual exposure
    trial3_visual = phase1_path + "bullseye.png"

    # fa file
    video_fa_list = ["FAH_34.mov", "FAH_40.mov", "FAH_60.mov", "FAH_98.mov"]
    video_fa = random.choice(video_fa_list)
    sound_fa = "fa_trial.wav"
    # tha file
    video_tha_list = ["THA_202.mov", "THA_206.mov", "THA_208.mov", "THA_214.mov"]
    video_tha = random.choice(video_tha_list)
    sound_tha = "tha_trial.wav"

    # output
    output = "./results/exp1_p1_results.csv"

    # Check condition ===============================================================================
    if condition_p1 == "fL-fE":
        left_video = video_path + video_fa
        right_video = video_path + video_tha
        sound_file = sound_path + sound_fa
        left = "fa"
        right = "tha"
        soundplay = "fa"
    elif condition_p1 == "fR-fE":
        left_video = video_path + video_tha
        right_video = video_path + video_fa
        sound_file = sound_path + sound_fa
        left = "tha"
        right = "fa"
        soundplay = "fa"
    elif condition_p1 == "fL-tE":
        left_video = video_path + video_fa
        right_video = video_path + video_tha
        sound_file = sound_path + sound_tha
        left = "fa"
        right = "tha"
        soundplay = "tha"
    elif condition_p1 == "fR-tE":
        left_video = video_path + video_tha
        right_video = video_path + video_fa
        sound_file = sound_path + sound_tha
        left = "tha"
        right = "fa"
        soundplay = "tha"
    else:
        raise ValueError('something is wrong in condition')

    # Background ====================================================================================
    background_black = (0, 0, 0)
    background_white = (255, 255, 255)
    # background_gray = (211, 211, 211)  # light gray
    psypsyinterface.clear_screen(screen, background_black)

    # Start experiment =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    write_result_phase1(output, subj, start_time, condition_p1, "1", trial_time, "attention-getter",
                        "NA", "NA", "NA")
    psypsyinterface.clear_screen(screen, background_black)

    # Trial 1: Baseline Trial =======================================================================
    # No sound ======================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyvideo.play_two_videos_loop(left_video, right_video, screen, duration=21000, audio=False)

    write_result_phase1(output, subj, start_time, condition_p1, "1", trial_time, "baseline",
                        left, right, "NA")
    psypsyinterface.clear_screen(screen, background_black)

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    write_result_phase1(output, subj, start_time, condition_p1, "2", trial_time, "attention-getter",
                        "NA", "NA", "NA")
    psypsyinterface.clear_screen(screen, background_black)

    # Trial 2: Baseline Trial  ======================================================================
    # swap videos ===================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyvideo.play_two_videos_loop(right_video, left_video, screen, duration=21000, audio=False)

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "2", trial_time, "baseline",
                        right, left, "NA")

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_white)
    write_result_phase1(output, subj, start_time, condition_p1, "3", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 3: auditory exposure trial ==============================================================
    # ===============================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyinterface.display_original_image(trial3_visual, screen, screen_width, screen_height)
    # presentation of sound file
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():  # sound playing
        continue

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "3", trial_time, "exposure",
                        left, right, "NA")

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_white)
    write_result_phase1(output, subj, start_time, condition_p1, "4", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 4: repeat trial 3 =======================================================================
    # ===============================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyinterface.display_original_image(trial3_visual, screen, screen_width, screen_height)
    # presentation of sound file
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():  # sound playing
        continue

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "4", trial_time, "exposure",
                        "NA", "NA", soundplay)

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "5", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 5 intersensory matching test trial ======================================================
    # ===============================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyvideo.play_two_videos_loop(left_video, right_video, screen, duration=45000, audio=False)

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "5", trial_time, "matching",
                        left, right, "NA")

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_white)
    write_result_phase1(output, subj, start_time, condition_p1, "6", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 6 auditory exposure trial ===============================================================
    # ===============================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyinterface.display_original_image(trial3_visual, screen, screen_width, screen_height)
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():  # sound playing
        continue

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "6", trial_time, "exposure",
                        "NA", "NA", soundplay)

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_white)
    write_result_phase1(output, subj, start_time, condition_p1, "7", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 7 repeat trial 6 ========================================================================
    # ===============================================================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyinterface.display_original_image(trial3_visual, screen, screen_width, screen_height)
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():  # sound playing
        continue

    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "7", trial_time, "exposure",
                        "NA", "NA", soundplay)

    # attention-getter ========================================
    # Loop attention.mov until there's a key press [SPACE]
    clip = VideoFileClip(video_attention_getter)
    psypsyvideo.play_video(clip, screen)
    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "8", trial_time, "attention-getter",
                        "NA", "NA", "NA")

    # Trial 8 Intersensory matching =================================================================
    # Same as trial 5 but video swapped =============================================================
    trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    psypsyvideo.play_two_videos_loop(right_video, left_video, screen, duration=45000, audio=False)
    psypsyinterface.clear_screen(screen, background_black)
    write_result_phase1(output, subj, start_time, condition_p1, "8", trial_time, "matching",
                        right, left, "NA")

    # ===============================================================================================
    # End of trial  =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*


def write_result_phase2(output, subj, start_time, condition_p2, trial_number, trial_time, sound_time,
                        trial_type, attention, left, right, trial_sound):
    f = open(output, 'a')
    result_list = [subj, start_time, condition_p2, trial_number, trial_time, sound_time, trial_type,
                   attention, left, right, trial_sound]
    result = "\t".join(result_list)
    print(result, file=f)
    f.close()


# Phase 2 Mispronunciation ============================================
def mispronunciation_2(subj, condition_p2, path, screen, screen_width, screen_height):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time

    # Path to files =================================================================================
    # path to experiment materials
    phase2_path = path["path"] + path["phase2"]

    # path to attention-getter
    attention_path = phase2_path + "attention-getters/"
    attention_videos = ["attention1.mov", "attention2.mov", "attention3.mov"]

    # Image Path
    image_path = phase2_path + "visual/"

    # Stimuli Path
    original_stimuli_file = "exp1_p2_stimuli.csv"

    # output
    output = "./results/exp1_p2_results.csv"

    # randomize stimuli list
    # repetition constraint
    constraints = {0: 0}

    # stimuli file destination
    result_file_path = "results/phase2/input/"
    psypsyaxb.randomisation_one_part(original_stimuli_file, result_file_path, "mispronunciation", subj, constraints)
    randomized_stimuli_file = result_file_path + "mispronunciation" + "_" + subj + ".csv"

    # Background ====================================================================================
    background_black = (0, 0, 0)
    background_white = (255, 255, 255)
    background_gray = (211, 211, 211)  # light gray
    psypsyinterface.clear_screen(screen, background_black)

    # Trial stimuli (shuffled)
    trial, header_index = psypsyio.read_stimuli(randomized_stimuli_file, "\t")

    # for i in range(2):
    for i in range(trial["trial_number"]):
        # Show an attention-getter movies chosen at random
        psypsyinterface.clear_screen(screen, background_black)
        attention_getter = random.choice(attention_videos)
        video_file = attention_path + attention_getter
        # play attention-getter video ===================================================================
        clip = VideoFileClip(video_file)
        psypsyvideo.play_video(clip, screen)
        psypsyinterface.clear_screen(screen, background_gray)

        # load image files
        image_target_obj = pygame.image.load(image_path + trial["target"][i] + ".png")
        image_competitor_obj = pygame.image.load(image_path + trial["competitor"][i] + ".png")

        if condition_p2 == "A":
            left_image = image_target_obj
            right_image = image_competitor_obj
            left = trial["target"][i]
            right = trial["competitor"][i]
        elif condition_p2 == "B":
            left_image = image_competitor_obj
            right_image = image_target_obj
            left = trial["competitor"][i]
            right = trial["target"][i]
        else:
            raise ValueError('something is wrong in condition')

        # resize image files
        left_size = left_image.get_rect().size
        right_size = right_image.get_rect().size

        # Calculate and rescale image to fit the screen
        # 40% empty space at the center, images occupy 30% left and right
        screen_30_percent = int(screen_width / 10 * 3)
        resize_left_height = int(screen_30_percent / left_size[0] * left_size[1])
        resize_right_height = int(screen_30_percent / right_size[0] * right_size[1])

        # rescale images
        image_left = pygame.transform.scale(left_image, (screen_30_percent, resize_left_height))
        image_right = pygame.transform.scale(right_image, (screen_30_percent, resize_right_height))

        # Display images
        trial_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

        screen.blit(image_left, (0, int((screen_height - resize_left_height) / 2)))
        screen.blit(image_right, (int(screen_width / 10 * 7), int((screen_height - resize_right_height) / 2)))
        pygame.display.flip()
        pygame.event.pump()
        pygame.event.clear()

        # 2s of silence
        pygame.time.wait(2000)

        # Play sound
        # Replace this line
        sound_file = trial["target"][i] + "_" + trial["extension"][i]
        sound_path = phase2_path + "wavs/" + sound_file + ".wav"
        # sound_file = trial["target"][i]
        # sound_path = phase2_path + "wavs/" + sound_file + ".wav"
        sound = pygame.mixer.Sound(sound_path)
        sound_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        sound.play()
        while pygame.mixer.get_busy():  # sound playing
            continue

        # Wait for 2.5s
        pygame.time.wait(2500)

        psypsyinterface.clear_screen(screen, background_gray)
        write_result_phase2(output, subj, start_time, condition_p2, str(i+1), trial_time, sound_time,
                            trial["trial_id"][i], attention_getter, left, right, sound_file)

    # End of Trial ==============================================================

    # Show red screen with message
    screen.fill((255, 0, 0))
    psypsyinterface.display_text(screen, "Move computer", font_size=90)

    # Wait for key press
    psypsyinterface.wait_for_space()



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


# MAIN =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
if __name__ == "__main__":
    # sys.argv
    skip_to_3 = False
    participant_id = sys.argv[1]
    if len(sys.argv) == 3:
        skip_to_3 = True
    else:
        skip_to_3 = False

    # Randomly assign participant to one of 4 conditions (fL-fE, fR-fE, fL-tE, fR-tE)  for phase 1 (AV matching)
    condition_list_p1 = ["fL-fE", "fR-fE", "fL-tE", "fR-tE"]
    condition_p1 = random.choice(condition_list_p1)

    # Randomly assign participant to one of 2 conditions (A and B)
    condition_list_p2 = ["A", "B"]
    condition_p2 = random.choice(condition_list_p2)

    # Randomly assign participant to one of 4 conditions (u-c, u-s, y-c, y-s) for phase 3
    condition_list_p3 = ["u-c", "u-s", "y-c", "y-s"]
    condition_p3 = random.choice(condition_list_p3)

    # Parameters  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
    # == Experiment path =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    path = {
            "path": "Exp_1_looking_time/",
            # Phase 1
            "phase1": "2018tsi_audiovisual/",
            # Phase 2
            "phase2": "2018tsi_lex/",
            # Phase 3
            "phase3": "2018tsi_nn/"
    }

    # == Program environment parameter =*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    background_gray = (211, 211, 211)  # light gray
    background_black = (0, 0, 0)  # black
    background_white = (255, 255, 255)  # white
    # Initialisation Pygame
    screen, screen_width, screen_height = psypsyinterface.initialisation_pygame(background_black)

    # Experiment procedure
    if skip_to_3:
        # Phase 3 =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
        habituation_3(participant_id, condition_p3, skip_to_3, path, screen, screen_width, screen_height)
    else:
        # Phase 1 =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
        av_matching_1(participant_id, condition_p1, path, screen)
        psypsyinterface.clear_screen(screen, background_black)

        # Phase 2 =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
        mispronunciation_2(participant_id, condition_p2, path, screen, screen_width, screen_height)
        psypsyinterface.clear_screen(screen, background_black)

        # Phase 3 =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
        habituation_3(participant_id, condition_p3, skip_to_3, path, screen, screen_width, screen_height)
