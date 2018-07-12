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


if __name__ == "__main__":
    # sys.argv
    participant_id = sys.argv[1]

    background_black = (0, 0, 0)  # black
    background_gray = (211, 211, 211)  # light gray
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

    condition_list_p1 = ["fL-fE", "fR-fE", "fL-tE", "fR-tE"]

    condition_p1 = random.choice(condition_list_p1)

    av_matching_1(participant_id, condition_p1, path, screen)
