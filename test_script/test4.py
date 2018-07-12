#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '1.0.0 (20180712)'
__maintainer__ = 'Shi YU'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'

import sys
import random
import pygame
from pygame.locals import *
from moviepy.editor import *
import datetime
import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyaxb as psypsyaxb
import libpsypsy.psypsyinterface as psypsyinterface
import libpsypsy.psypsyvideo as psypsyvideo
import re


def write_result_exp3(output, subj, exp_start, trial_number,
                      contrast, target_side,
                      target_video, trial_start,
                      on, off, rt, response_side, correct):
    f = open(output, 'a')
    result_list = [subj, exp_start, trial_number,
                   contrast, target_side,
                   target_video, trial_start,
                   on, off, rt, response_side, correct]
    result = "\t".join(result_list)
    print(result, file=f)
    f.close()


def exp3_av_matching(participant_id):
    exp_start = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time

    background_white = (255, 255, 255)  # white
    background_black = (0, 0, 0)  # black
    # Initialisation Pygame
    screen, screen_width, screen_height = psypsyinterface.initialisation_pygame_mouse(background_white)
    psypsyinterface.clear_screen(screen, background_white)

    path = {
        "path": "Exp_3_av_matching/",
        "instructions": "instructions/",
        "visual": "visual/",
        "adults": "adults/"
    }

    # Instructions =*=*=*=*=*=*=*=*=*=*=*=*=*=*
    instructions = ["instructions1.wav", "instructions2.wav", "instructions3.wav",
                    "instructions4.wav", "instructions5.wav"]
    instruction_path = path["path"] + path["instructions"]

    # visual =*=*=*=*=*=*=*=*=*=*=*=*=*=*
    visual_path = path["path"] + path["visual"]
    ear_file = visual_path + "ear.png"
    eye_file = visual_path + "eye.png"
    finger_file = visual_path + "finger.png"
    box_file = visual_path + "box.png"

    # Video  =*=*=*=*=*=*=*=*=*=*=*=*=*=*
    video_path = path["path"] + path["adults"]
    left_video = video_path + "BAH_44.mov"
    right_video = video_path + "VAH_24.mov"

    # Audio
    ba_sound = video_path + "BAH_44.wav"

    # Repetition constraints for trials
    constraints = {3: 2}

    # Stimuli input file
    stimuli_file = "exp3_trial.csv"

    # Result file ==============================================================================
    result_file = "results/exp3_results.csv"

    # Load Images & calculate size
    ear = pygame.image.load(ear_file)
    eye = pygame.image.load(eye_file)
    finger = pygame.image.load(finger_file)
    box = pygame.image.load(box_file)

    ear_size = ear.get_rect().size
    eye_size = eye.get_rect().size
    finger_size = finger.get_rect().size
    box_size = box.get_rect().size

    # Play instructions1.wav (says there are 3 phases) ================================================
    instruction1 = instruction_path + instructions[0]
    instruction1_sound = pygame.mixer.Sound(instruction1)
    instruction1_sound.play()  # play instruction
    while pygame.mixer.get_busy():  # Instruction playing
        continue
    psypsyinterface.wait_for_click()
    psypsyinterface.clear_screen(screen, background_white)

    # Make ear appear and play instructions2.wav (it will explain the procedure for the listening phase)
    psypsyinterface.display_original_image(ear_file, screen, screen_width, screen_height)
    instruction2 = instruction_path + instructions[1]
    instruction2_sound = pygame.mixer.Sound(instruction2)
    instruction2_sound.play()  # play instruction
    while pygame.mixer.get_busy():  # Instruction playing
        continue
    psypsyinterface.wait_for_click()
    psypsyinterface.clear_screen(screen, background_white)

    # Make eye appear and play instructions3.wav (same for viewing phase) ==============================
    psypsyinterface.display_original_image(eye_file, screen, screen_width, screen_height)
    instruction3 = instruction_path + instructions[2]
    instruction3_sound = pygame.mixer.Sound(instruction3)
    instruction3_sound.play()  # play instruction
    while pygame.mixer.get_busy():  # Instruction playing
        continue
    psypsyinterface.wait_for_click()
    psypsyinterface.clear_screen(screen, background_white)

    # Show the arrow and play instructions4.wav (same for choice) ======================================
    psypsyinterface.display_original_image(finger_file, screen, screen_width, screen_height)
    instruction4 = instruction_path + instructions[3]
    instruction4_sound = pygame.mixer.Sound(instruction4)
    instruction4_sound.play()  # play instruction
    while pygame.mixer.get_busy():  # Instruction playing
        continue
    psypsyinterface.wait_for_click()
    psypsyinterface.clear_screen(screen, background_white)

    # One trial for practice with ba-by ================================================================
    trial_start = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    # Audio-only
    ear_resize = pygame.transform.scale(ear, (int(screen_width * 0.3), int(screen_width * 0.3 / ear_size[0] * ear_size[1])))
    ear_position = (int((screen_width - (screen_width * 0.3))/2), 0)
    screen.blit(ear_resize, ear_position)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    bah = pygame.mixer.Sound(ba_sound)
    for j in range(2):  # play twice ba sound
        bah.play()  # play sound
        while pygame.mixer.get_busy():  # sound playing
            continue
        pygame.time.wait(500)

    psypsyinterface.clear_screen(screen, background_white)
    # Video-only
    eye_resize = pygame.transform.scale(eye, (int(screen_width * 0.3),
                                              int(screen_width * 0.3 / eye_size[0] * eye_size[1])))
    eye_position = (int((screen_width - (screen_width * 0.3))/2), 0)
    screen.blit(eye_resize, eye_position)
    left_video_clip = VideoFileClip(left_video)
    right_video_clip = VideoFileClip(right_video)
    time_video_on = pygame.time.get_ticks()
    psypsyvideo.play_two_videos_audio(left_video_clip, right_video_clip, "left", screen)

    # Show black screen with two boxes where the videos were & the finger
    psypsyinterface.clear_screen(screen, background_white)

    # Response: visual
    box_resize = pygame.transform.scale(box, (int(screen_width * 0.3),
                                              int(screen_width * 0.3 / box_size[0] * box_size[1])))
    box_size_2 = box_resize.get_rect().size
    box_left_position = (0, int((screen_height - box_size_2[1]) / 2))
    box_right_position = (int(screen_width - box_size_2[0]), int((screen_height - box_size_2[1]) / 2))
    position_box_left = screen.blit(box_resize, box_left_position)
    position_box_right = screen.blit(box_resize, box_right_position)

    finger_resize = pygame.transform.scale(finger, (int(screen_width * 0.1),
                                                    int(screen_width * 0.1 / finger_size[0] * finger_size[1])))
    finger_position = (int((screen_width - (screen_width * 0.1)) / 2), 0)
    screen.blit(finger_resize, finger_position)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()

    response = False
    while not response:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                raise Exception
            elif e.type == MOUSEBUTTONDOWN:
                # set x, y positions of the mouse click
                x, y = e.pos
                if position_box_left.collidepoint(x, y):
                    # print("click on a")
                    response_time = [pygame.time.get_ticks()]
                    response_type = ["left"]
                    response = True
                elif position_box_right.collidepoint(x, y):
                    # print("click on b")
                    response_time = [pygame.time.get_ticks()]
                    # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                    response_type = ["right"]
                    response = True

    off = response_time[0]
    rt = off - time_video_on
    response_side = response_type[0]

    if response_side == "left":
        correct = "1"
    else:
        correct = "0"

    write_result_exp3(result_file, str(participant_id), exp_start, "0",
                      "N", "left",
                      "BAH_44.mov", trial_start,
                      str(time_video_on), str(off), str(rt), response_side, correct)
    # Wait for click to advance, log response
    psypsyinterface.wait_for_click()
    psypsyinterface.clear_screen(screen, background_white)

    # Play instructions5.wav ===========================================================================
    # (it will ask the participant to tell the experimenter if they have any questions)
    instruction5 = instruction_path + instructions[4]
    instruction5_sound = pygame.mixer.Sound(instruction5)
    instruction5_sound.play()  # play instruction
    while pygame.mixer.get_busy():  # Instruction playing
        continue
    # Continue with a click anywhere on the scree
    psypsyinterface.wait_for_click()

    # Test trials
    # randomisation
    psypsyaxb.randomisation_one_part(stimuli_file, "results/exp3/", "test_trial",
                                     participant_id, constraints)
    trial_file = "results/exp3/test_trial_" + str(participant_id) + ".csv"
    trial, header_index = psypsyio.read_stimuli(trial_file, "\t")
    for i in range(trial["trial_number"]):
        psypsyinterface.clear_screen(screen, background_black)
        trial_start = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

        psypsyinterface.clear_screen(screen, background_white)
        # Audio-only trial ===================================
        screen.blit(ear_resize, ear_position)
        pygame.display.flip()
        pygame.event.pump()
        pygame.event.clear()
        target_sound = pygame.mixer.Sound(video_path + trial["target_audio"][i])
        for j in range(2):  # play twice ba sound
            target_sound.play()  # play sound
            while pygame.mixer.get_busy():  # sound playing
                continue
            pygame.time.wait(500)

        # Video-only trial ====================================
        psypsyinterface.clear_screen(screen, background_white)
        screen.blit(eye_resize, eye_position)

        left_video = video_path + trial["left"][i]
        right_video = video_path + trial["right"][i]
        left_video_clip = VideoFileClip(left_video)
        right_video_clip = VideoFileClip(right_video)
        audioside = trial["target_side"][i]
        time_video_on = pygame.time.get_ticks()
        psypsyvideo.play_two_videos_audio(left_video_clip, right_video_clip, audioside, screen)
        psypsyinterface.clear_screen(screen, background_white)

        position_box_left = screen.blit(box_resize, box_left_position)
        position_box_right = screen.blit(box_resize, box_right_position)
        screen.blit(finger_resize, finger_position)
        pygame.display.flip()
        pygame.event.pump()
        pygame.event.clear()

        time_video_off = pygame.time.get_ticks()

        response = False
        while not response:
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    raise Exception
                elif e.type == MOUSEBUTTONDOWN:
                    # set x, y positions of the mouse click
                    x, y = e.pos
                    if position_box_left.collidepoint(x, y):
                        # print("click on a")
                        response_time = [pygame.time.get_ticks()]
                        response_type = ["left"]
                        response = True
                    elif position_box_right.collidepoint(x, y):
                        # print("click on b")
                        response_time = [pygame.time.get_ticks()]
                        response_type = ["right"]
                        response = True
        off = response_time[0]
        rt = off - time_video_on
        response_side = response_type[0]

        if response_side == trial["target_side"][i]:
            correct = "1"
        else:
            correct = "0"

        write_result_exp3(result_file, str(participant_id), exp_start, str(i+1),
                          trial["contrasts"][i], trial["target_side"][i],
                          trial["target_video"][i], trial_start,
                          str(time_video_on), str(off), str(rt), response_side, correct)

        psypsyinterface.clear_screen(screen, background_black)


if __name__ == "__main__":
    # sys.argv
    participant_id = sys.argv[1]
    exp3_av_matching(participant_id)



