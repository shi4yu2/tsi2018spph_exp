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


# =====================================================

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

    condition_list_p2 = ["A", "B"]
    condition_p2 = random.choice(condition_list_p2)

    mispronunciation_2(participant_id, condition_p2, path, screen, screen_width, screen_height)


