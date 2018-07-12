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
import datetime
import pygame
from pygame.locals import *
from moviepy.editor import *
import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyinterface as psypsyinterface
import libpsypsy.psypsyaxb as psypsyaxb
import libpsypsy.psypsyvideo as psypsyvideo

# ============================================
#                                            =
# Tsimane children and adults 2018: AXB task =
#                                            =
# ============================================


# First phase: picture-word pairing trials =================================================
def exposure_phase(pairing, path, screen, screen_width, screen_height):
    keys = list(pairing.keys())

    # words presentation in same order
    for key in keys:
        # we first present a fixed female voice with image
        sound_file = path["path"] + path["female"] + key + "1a" + ".wav"
        image_file = path["path"] + path["image"] + pairing[key] + ".jpg"

        psypsyinterface.display_image(image_file, screen, screen_width, screen_height)
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        while pygame.mixer.get_busy():  # sound playing
            continue
        psypsyinterface.wait_for_click()

    # shuffled across participants
    random.shuffle(keys)
    for key in keys:
        # we first present a fixed female voice with image
        sound_file = path["path"] + path["female"] + key + "1a" + ".wav"
        image_file = path["path"] + path["image"] + pairing[key] + ".jpg"

        psypsyinterface.display_image(image_file, screen, screen_width, screen_height)
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        while pygame.mixer.get_busy():  # sound playing
            continue
        psypsyinterface.wait_for_click()

    return keys


def write_result_axb(output, subj, exp_start, pair, trial_number, contrast, trial_condition,
                     target, trial_start,
                     start_a, end_a, start_x, end_x, start_b, end_b,
                     art, rt, side, correct, feedback):
    f = open(output, 'a')
    result_list = [subj, exp_start, pair, str(trial_number), contrast, trial_condition,
                   target, trial_start,
                   str(start_a), str(end_a), str(start_x), str(end_x), str(start_b), str(end_b),
                   str(art), str(rt), side, str(correct), str(feedback)]
    result = "\t".join(result_list)
    print(result, file=f)
    f.close()


def axb_trial(subj, pairing, pair, exp_start, path, trial_condition, trial_file,
              screen, screen_width, screen_height, background):
    # Import stimuli files =========================================
    # stimuli are organised in a python dictionary type, to view the content use print()
    trial, header_index = psypsyio.read_stimuli(trial_file, "\t")

    # Path =====================================================================================
    feedback_path = path["path"] + path["feedback"]
    female_path = path["path"] + path["female"]
    male_path = path["path"] + path["male"]
    noise_path = path["path"] + path["noise"]
    img_path = path["path"] + path["image"]

    # Result file ==============================================================================
    result_file = "results/axb_result.csv"

    # Feedback sound ===========================================================================
    positive_feedback_sound = feedback_path + "positive" + ".wav"
    negative_feedback_sound = feedback_path + "negative" + ".wav"

    # Initialize counts for feedback
    nb_trials = 0
    response_count = 0

    # Check trial condition
    if trial_condition == "TS":
        ab_path = female_path
        x_path = female_path
        feedback = 1
    elif trial_condition == "TN":
        ab_path = female_path
        x_path_choice = [male_path, noise_path]
        x_path = female_path
        feedback = 1
    elif trial_condition == "S":
        ab_path = female_path
        x_path = female_path
        feedback = 0
    elif trial_condition == "N":
        ab_path = female_path
        x_path = noise_path
        feedback = 0
    elif trial_condition == "V":
        ab_path = female_path
        x_path = male_path
        feedback = 0
    else:
        raise ValueError('Wrong trial condition')

    # Start trial ==============================================================================
    for i in range(trial["trial_number"]):
        nb_trials += 1
        screen.fill(background)
        pygame.display.flip()
        # participant initiate each trial by pressing on the space bar
        # psypsyinterface.wait_for_click()

        # load sound files
        # all of the stimuli were presented in the clear, with the same speaker’s voice.
        stimulus_a = ab_path + trial["A"][i] + ".wav"
        stimulus_b = ab_path + trial["B"][i] + ".wav"
        if trial_condition == "TN":
            x_path = random.choice(x_path_choice)
        stimulus_x = x_path + trial["X"][i] + ".wav"

        sound_path = [stimulus_a, stimulus_x, stimulus_b]

        # Load stimuli & Compute sound stimuli duration
        mixed_sounds, duration_sounds = psypsyinterface.mix_sound_stimuli(sound_path)

        # Calculate size of images ==========================================================
        axb_img_width = int(screen_width / 10 * 3)
        axb_img_height = int(screen_height / screen_width * axb_img_width)

        # load image files
        image_a_file = pairing[trial["A"][i][:-2]]
        image_x_file = pairing[trial["X"][i][:-2]]
        image_b_file = pairing[trial["B"][i][:-2]]
        image_a = pygame.image.load(img_path + image_a_file + ".jpg")
        image_a_obj = pygame.transform.scale(image_a, (axb_img_width, axb_img_height))
        image_x = pygame.image.load(img_path + image_x_file + ".jpg")
        image_x_obj = pygame.transform.scale(image_x, (axb_img_width, axb_img_height))
        image_b = pygame.image.load(img_path + image_b_file + ".jpg")
        image_b_obj = pygame.transform.scale(image_b, (axb_img_width, axb_img_height))

        image_leaf = pygame.image.load(img_path + "leaf" + ".jpg")
        image_leaf_obj = pygame.transform.scale(image_leaf, (axb_img_width, axb_img_height))

        image_a_position = (0, int((screen_height - axb_img_height)/2))
        image_x_position = (int((screen_width - axb_img_width)/2), int((screen_height - axb_img_height)/2))
        image_b_position = (int(screen_width - axb_img_width), int((screen_height - axb_img_height)/2))

        # Play A ==============
        trial_start = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time
        start_sound_a = pygame.time.get_ticks()
        position_a = screen.blit(image_a_obj, image_a_position)
        pygame.display.flip()
        pygame.event.pump()
        pygame.event.clear()

        mixed_sounds[0].play()  # PLAY SOUND A
        while pygame.mixer.get_busy():  # sound playing
            continue
        end_sound_a = pygame.time.get_ticks()

        while pygame.time.get_ticks() - end_sound_a < 1000:
            continue
        pygame.event.pump()
        pygame.event.clear()  # clear event and wait for response

        # Play X and B and record response (Type, Time) =============
        xb_sequence = [mixed_sounds[1], mixed_sounds[2]]
        xb_measures = []
        response = False
        response_type = []
        response_time = []

        # indication for X and B
        # index_b == 0: ISI after X
        # index_b == 1: ISI after B
        index_b = 0

        for s in xb_sequence:
            # get start point of the sound
            duration = int(round(pygame.mixer.Sound.get_length(s), 3) * 1000)
            start_sound = pygame.time.get_ticks()
            xb_measures.append(start_sound)
            if index_b == 1:
                position_b = screen.blit(image_b_obj, image_b_position)
                pygame.display.flip()
                pygame.event.pump()
                pygame.event.clear()
            else:
                screen.blit(image_leaf_obj, image_x_position)
                pygame.display.flip()
                pygame.event.pump()
                pygame.event.clear()

            s.play()  # play sound

            isi_post = 1000

            while pygame.mixer.get_busy() and not response \
                    or pygame.time.get_ticks() - start_sound <= duration + isi_post:
                if index_b == 0:
                    if not response and pygame.time.get_ticks() - start_sound > 300:
                        for e in pygame.event.get():
                            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                                raise Exception
                            elif e.type == MOUSEBUTTONDOWN:
                                # set x, y positions of the mouse click
                                x, y = e.pos
                                if position_a.collidepoint(x, y):
                                    # print("click on a")
                                    response_time = [pygame.time.get_ticks()]
                                    response_type = ["A"]
                                    # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    response = True
                                    screen.blit(image_a_obj, image_x_position)
                                    pygame.display.flip()
                                    pygame.event.pump()
                                    pygame.event.clear()
                                elif position_b.collidepoint(x, y):
                                    # print("click on b")
                                    response_time = [pygame.time.get_ticks()]
                                    # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    response_type = ["B"]
                                    response = True
                                    screen.blit(image_b_obj, image_x_position)
                                    pygame.display.flip()
                                    pygame.event.pump()
                                    pygame.event.clear()
                else:
                    if not response:
                        for e in pygame.event.get():
                            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                                raise Exception
                            elif e.type == MOUSEBUTTONDOWN:
                                # set x, y positions of the mouse click
                                x, y = e.pos
                                if position_a.collidepoint(x, y):
                                    # print("click on a")
                                    response_time = [pygame.time.get_ticks()]
                                    response_type = ["A"]
                                    # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    response = True
                                    screen.blit(image_a_obj, image_x_position)
                                    pygame.display.flip()
                                    pygame.event.pump()
                                    pygame.event.clear()
                                elif position_b.collidepoint(x, y):
                                    # print("click on b")
                                    response_time = [pygame.time.get_ticks()]
                                    # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    response_type = ["B"]
                                    response = True
                                    screen.blit(image_b_obj, image_x_position)
                                    pygame.display.flip()
                                    pygame.event.pump()
                                    pygame.event.clear()

            # Get end point of the sound
                xb_measures.append(pygame.time.get_ticks() - isi_post)

            index_b += 1

        if not response:
            while not response:
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                        raise Exception
                    elif e.type == MOUSEBUTTONDOWN:
                        # set x, y positions of the mouse click
                        x, y = e.pos
                        if position_a.collidepoint(x, y):
                            # print("click on a")
                            response_time = [pygame.time.get_ticks()]
                            response_type = ["A"]
                            # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                            response = True
                            screen.blit(image_a_obj, image_x_position)
                            pygame.display.flip()
                            pygame.event.pump()
                            pygame.event.clear()
                        elif position_b.collidepoint(x, y):
                            # print("click on b")
                            response_time = [pygame.time.get_ticks()]
                            # absolute_response_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                            response_type = ["B"]
                            response = True
                            screen.blit(image_b_obj, image_x_position)
                            pygame.display.flip()
                            pygame.event.pump()
                            pygame.event.clear()
            else:
                pass

        # Get measures
        start_sound_x = xb_measures[0]
        end_sound_x = xb_measures[1]
        start_sound_b = xb_measures[2]
        end_sound_b = xb_measures[3]

        # Handle empty response
        # response time =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*
        if response_time != []:
            response_time_s = response_time[0]
            real_rt = response_time_s - start_sound_b
        else:
            response_time_s = 0
            real_rt = 0

        # response type =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*
        if response_type != []:
            response_type_s = response_type[0]
        else:
            response_type_s = "NA"

        if response_type_s == trial["target"][i]:
            correct = 1
            response_count += 1
            if trial_condition == "TN" or trial_condition == "TS":
                feedback = 1
            elif response_count % 4 == 0:
                feedback = 1
            else:
                feedback = 0

            if feedback == 1:
                if response_type_s == "A":
                    feedback_img = image_a_obj
                elif response_type_s == "B":
                    feedback_img = image_b_obj
                pygame.time.wait(700)
                positive_feedback = pygame.mixer.Sound(positive_feedback_sound)
                positive_feedback.play()
                while pygame.mixer.get_busy():  # sound playing
                    # Enlarge image when correct response
                    feedback_img = pygame.transform.scale(feedback_img,
                                                          (int(axb_img_width * 1.3), int(axb_img_height * 1.3)))
                    feedback_img_width = feedback_img.get_rect().size[0]
                    feedback_img_height = feedback_img.get_rect().size[1]
                    feedback_img_position = (int((screen_width - feedback_img_width) / 2),
                                             int((screen_height - feedback_img_height) / 2))
                    screen.blit(feedback_img, feedback_img_position)
                    pygame.display.flip()
                    pygame.event.pump()
                    pygame.event.clear()
                    pygame.time.wait(20)

        elif response_type_s == "NA":
            correct = 0
        else:
            correct = 0
            if trial_condition == "TN" or trial_condition == "TS":
                pygame.time.wait(700)
                screen.blit(image_x_obj, image_x_position)
                pygame.display.flip()
                pygame.event.pump()
                pygame.event.clear()
                negative_feedback = pygame.mixer.Sound(negative_feedback_sound)
                negative_feedback.play()
                while pygame.mixer.get_busy():  # sound playing
                    continue

        write_result_axb(result_file, subj, exp_start, pair, nb_trials, trial["contrast"][i], trial_condition,
                         trial["target"][i], trial_start,
                         start_sound_a, end_sound_a, start_sound_x, end_sound_x, start_sound_b, end_sound_b,
                         response_time_s,
                         real_rt, response_type_s, correct, feedback)

        pygame.time.wait(1000)
        screen.fill(background)
        pygame.display.flip()
        pygame.event.pump()
        pygame.event.clear()
        pygame.time.wait(1000)


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
    # get participant id
    participant_id = sys.argv[1]

    exp_start = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  # get current date time

    # Trial stimuli files
    training_file = "Exp_2_trial/practice.csv"
    trial_file = "Exp_2_trial/trial.csv"
    # Repetition constraints for trials
    constraints_training = {4: 2}
    constraints = {4: 2}

    path = {
        "path": "Exp_2_axb/2018tsi_axb/",
        "image": "visual/",
        "male": "male/",
        "female": "female/",
        "noise": "noise/",
        "feedback": "feedback/"
    }

    trial_block = {
        "training_silent": "TS",
        "silent": "S",
        "training_noise": "TN",
        "noise": "N",
        "voice": "V"
    }

    # Initialisation word; sound
    wordList = ["rodent", "snake", "spider", "bird", "lizard"]
    soundList = ["afa", "ava", "asa", "ama", "aza"]

    # Pairing randomization - dict{sound: word} ================================
    random.shuffle(soundList)
    pairing = dict(zip(soundList, wordList))
    pair = ""
    for key, value in pairing.items():
        pair = pair + key + "-" + value + "_"
    # Get sound_word pair
    pair = pair[0:-1]

    # Parameter  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
    # == Program environment parameter  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    font = "helvetica"
    background = (211, 211, 211)  # gray
    isi = 1000

    instruction_path = path["path"] + path["feedback"]
    instruction = ["instructions1.wav", "instructions2.wav", "instructions3.wav", "instructions4.wav"]

    # initialise pygame environment
    screen, screen_width, screen_height = psypsyinterface.initialisation_pygame(background)

    # # Experiment Start ================================================================================================
    # # =================================================================================================================
    #
    # # Instruction 1 =*=*=**=*=*=*=*=*=*=*=*=*=*
    # # Play instructions1.wav (it will explain the procedure for the 5 picture-word blocks)
    # # Continue with a click anywhere on the screen
    # psypsyinterface.clear_screen(screen, background)
    # instruction1 = instruction_path + instruction[0]
    # instruction1_sound = pygame.mixer.Sound(instruction1)
    # instruction1_sound.play()  # play instruction
    # while pygame.mixer.get_busy():  # Instruction playing
    #     continue
    # psypsyinterface.wait_for_click()
    #
    # # 1. Exposure  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # render the stimuli semantically meaningful and provide more context to the rest.
    # # 5 picture-word pairing trials, repeated (total 10 trials)
    #
    # psypsyinterface.clear_screen(screen, background)
    # random_keys = exposure_phase(pairing, path, screen, screen_width, screen_height)
    # random_exposure = "_".join(random_keys)
    #
    # # Instrucion 2 =*=*=**=*=*=*=*=*=*=*=*=*=*
    # # Play instructions2.wav (it will explain the procedure for the trials)
    # # Show a picture on each left & right slots and the leaf in the middle (test trial configuration)
    # # Continue with a click anywhere on the screen
    # psypsyinterface.clear_screen(screen, background)
    # instruction2 = instruction_path + instruction[1]
    # instruction2_sound = pygame.mixer.Sound(instruction2)
    # instruction2_sound.play()  # PLAY SOUND A
    # while pygame.mixer.get_busy():  # Instruction playing
    #     continue
    # psypsyinterface.wait_for_click()
    #
    # # 2. Practice  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # 8 training in silence trials
    # # randomisation
    # psypsyaxb.randomisation_one_part(training_file, "results/axb/", "training_2",
    #                                  participant_id, constraints_training)
    # training_2_input = "results/axb/training_2_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["training_silent"], training_2_input,
    #           screen, screen_width, screen_height, background)
    #
    # # Instruction 3 =*=*=**=*=*=*=*=*=*=*=*=*=*
    # # Play instructions3.wav (it will ask the participant to tell the experimenter if they have any questions)
    # # Continue with a click anywhere on the screen
    # psypsyinterface.clear_screen(screen, background)
    # instruction3 = instruction_path + instruction[2]
    # instruction3_sound = pygame.mixer.Sound(instruction3)
    # instruction3_sound.play()  # play instruction
    # while pygame.mixer.get_busy():  # Instruction playing
    #     continue
    # psypsyinterface.wait_for_click()
    #
    # # 3. 48 test in silence =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/", "trial_3",
    #                                  participant_id, constraints)
    # trial_3_input = "results/axb/trial_3_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["silent"], trial_3_input,
    #           screen, screen_width, screen_height, background)
    #
    # # 4. Practice: 8 training with noise/voice =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(training_file, "results/axb/", "training_4",
    #                                  participant_id, constraints_training)
    # training_4_input = "results/axb/training_4_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["training_noise"], training_4_input,
    #           screen, screen_width, screen_height, background)
    #
    # # 5. 48 test noise =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/", "trial_5",
    #                                  participant_id, constraints)
    # trial_5_input = "results/axb/trial_5_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["noise"], trial_5_input,
    #           screen, screen_width, screen_height, background)
    #
    # # 6. 48 test voice =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/" "trial_6",
    #                                  participant_id, constraints)
    # trial_6_input = "results/axb/trial_6_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["voice"], trial_6_input,
    #           screen, screen_width, screen_height, background)
    #
    # # Instruction 4 =*=*=**=*=*=*=*=*=*=*=*=*=*
    # # Play  instructions4.wav (it will ask the participant to take a short break)
    # # Continue with a click anywhere on the screen
    # psypsyinterface.clear_screen(screen, background)
    # instruction4 = instruction_path + instruction[3]
    # instruction4_sound = pygame.mixer.Sound(instruction4)
    # instruction4_sound.play()  # play instruction
    # while pygame.mixer.get_busy():  # Instruction playing
    #     continue
    # psypsyinterface.wait_for_click()
    #
    # # 7. 48 test silent =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/", "trial_7",
    #                                  participant_id, constraints)
    # trial_7_input = "results/axb/trial_7_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["silent"], trial_7_input,
    #           screen, screen_width, screen_height, background)
    #
    # # 8. 48 test noise  =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/", "trial_8",
    #                                  participant_id, constraints)
    # trial_8_input = "results/axb/trial_8_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["noise"], trial_8_input,
    #           screen, screen_width, screen_height, background)
    #
    # # 9. 48 test voice  =*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # # randomisation
    # psypsyaxb.randomisation_one_part(trial_file, "results/axb/" "trial_9",
    #                                  participant_id, constraints)
    # trial_9_input = "results/axb/trial_9_" + str(participant_id) + ".csv"
    # axb_trial(participant_id, pairing, pair, exp_start, path, trial_block["voice"], trial_9_input,
    #           screen, screen_width, screen_height, background)
    # End Exp

    # AV matching
    exp3_av_matching(participant_id)
    pygame.quit()

