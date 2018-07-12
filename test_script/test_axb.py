import sys
import random
import pygame
from pygame.locals import *
import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyinterface as psypsyinterface

# participant_id = sys.argv[1]

# path = {
#     "path": "Exp_2_axb/2018tsi_axb/",
#     "image": "visual/",
#     "male": "male/",
#     "female": "female/",
#     "noise": "noise/",
#     "feedback": "feedback/"
# }
#
# # Initialisation word; sound
# wordList = ["rodent", "snake", "spider", "bird", "lizard"]
# soundList = ["afa", "ava", "asa", "ama", "aza"]
#
# # # Pairing randomization - dict{sound: word} ================================
# # random.shuffle(soundList)
# # pairing = dict(zip(soundList, wordList))
# # print(pairing)
# # pair = ""
# # for key, value in pairing.items():
# #     pair = pair + key + "-" + value + "_"
# # pair = pair[0:-1]
# # print(pair)
# #
# #
# # font = "helvetica"
# # background = (150, 150, 150)  # gray
# # isi = 1000
# #
# # # screen, screen_width, screen_height = psypsyinterface.initialisation_pygame_mouse(background)
# # pygame.init()
# # image_a = pygame.image.load(path["path"] + path["image"] + "spider" + ".jpg")
# # img_size = image_a.get_rect().size
# # print(img_size[1])
#
#
#
#
# if __name__ == "__main__":
#     # participant_id = sys.argv[1]
#
#     path = {
#         "path": "Exp_2_axb/2018tsi_axb/",
#         "image": "visual/",
#         "male": "male/",
#         "female": "female/",
#         "noise": "noise/",
#         "feedback": "feedback/"
#     }
#
#     # Initialisation word; sound
#     wordList = ["rodent", "snake", "spider", "bird", "lizard"]
#     soundList = ["afa", "ava", "asa", "ama", "aza"]
#
#     # Pairing randomization - dict{sound: word} ================================
#     random.shuffle(soundList)
#     pairing = dict(zip(soundList, wordList))
#     pair = ""
#     for key, value in pairing.items():
#         pair = pair + key + "-" + value + "_"
#     pair = pair[0:-1]
#
#     # First phase =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#     # render the stimuli semantically meaningful and provide more context to the rest.
#
#     # experiment procedure
#
#     # Parameter  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
#     # == Program environment parameter  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#     font = "helvetica"
#     background = (150, 150, 150)  # gray
#     isi = 1000
#
#     screen, screen_width, screen_height = psypsyinterface.initialisation_pygame_mouse(background)
#
#     # First phase =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
#     # psypsyinterface.display_text(screen, "first phase")
#     # psypsyinterface.wait_for_space()
#     # psypsyinterface.clear_screen(screen, background)
#     # first_phase(pairing, path, screen, screen_width, screen_height)
#
#     # Practice Trial =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#     # Input file
#     trial, header_index = psypsyio.read_stimuli(path["path"] + "trial/training.csv", "\t")
#     # ! Do randomization !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     # ! Do output !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#     psypsyinterface.clear_screen(screen, background)
#     psypsyinterface.display_text(screen, "practice trial")
#     psypsyinterface.wait_for_space()
#     practice_trial(trial, path, pairing, isi, screen, screen_width, screen_height, background)
#
#     # Practice Trial =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*


print(1 and 0)