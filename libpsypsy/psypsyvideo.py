#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PSYchology Python by Shi Yu
Video playback
"""


# Todo :
#

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180704)'
__maintainer__ = 'ShY'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'


import threading
import time
import pygame as pg
import numpy as np
from moviepy.editor import *


def imdisplay(imarray, screen=None, position=(0, 0)):
    """Splashes the given image array on the given pygame screen """
    a = pg.surfarray.make_surface(imarray.swapaxes(0, 1))
    if screen is None:
        screen = pg.display.set_mode(imarray.shape[:2][::-1])

    screen.blit(a, position)
    pg.display.flip()


def show(clip, t=0, with_mask=True, interactive=False):
    """
    Splashes the frame of clip corresponding to time ``t``.

    Parameters
    ------------

    t
      Time in seconds of the frame to display.

    with_mask
      ``False`` if the clip has a mask but you want to see the clip
      without the mask.

    """

    if isinstance(t, tuple):
        t = cvsecs(*t)

    if with_mask and (clip.mask is not None):
        import moviepy.video.compositing.CompositeVideoClip as cvc
        clip = cvc.CompositeVideoClip([clip.set_pos((0, 0))])
    img = clip.get_frame(t)
    imdisplay(img)

    if interactive:
        result = []
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Keyboard interrupt")
                        return result
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    rgb = img[y, x]
                    result.append({'position': (x, y), 'color': rgb})
                    print("position, color : ", "%s, %s" %
                          (str((x, y)), str(rgb)))
            time.sleep(.03)


def play_video(clip, screen, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000,
            audio_nbytes=2, fullscreen=False):
    """
    Displays the clip in a window, at the given frames per second
    (of movie) rate. It will avoid that the clip be played faster
    than normal, but it cannot avoid the clip to be played slower
    than normal if the computations are complex. In this case, try
    reducing the ``fps``.

    Parameters
    ------------

    fps
      Number of frames per seconds in the displayed video.

    audio
      ``True`` (default) if you want the clip's audio be played during
      the preview.

    audio_fps
      The frames per second to use when generating the audio sound.

    fullscreen
      ``True`` if you want the preview to be displayed fullscreen.

    """
    # Center video on the screen
    # get clip size
    size = clip.size
    # get screen size
    display_info = pg.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    position = (int((screen_width - size[0]) / 2), int((screen_height - size[1]) / 2))

    if fullscreen:
        flags = pg.FULLSCREEN
    else:
        flags = 0

    # compute and splash the first image
    # screen = pg.display.set_mode(clip.size, flags)

    audio = audio and (clip.audio is not None)

    if audio:
        # the sound will be played in parrallel. We are not
        # parralellizing it on different CPUs because it seems that
        # pygame and openCV already use several cpus it seems.

        # two synchro-flags to tell whether audio and video are ready
        videoFlag = threading.Event()
        audioFlag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(target=clip.audio.preview,
                                       args=(audio_fps,
                                             audio_buffersize,
                                             audio_nbytes,
                                             audioFlag, videoFlag))
        audiothread.start()

    img = clip.get_frame(0)
    imdisplay(img, screen, position)
    if audio:  # synchronize with audio
        videoFlag.set()  # say to the audio: video is ready
        audioFlag.wait()  # wait for the audio to be ready

    result = []

    t0 = time.time()
    for t in np.arange(1.0 / fps, clip.duration - .001, 1.0 / fps):

        img = clip.get_frame(t)

        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if audio:
                    videoFlag.clear()
                print("Interrupt")
                return True
            # elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            elif event.type == pg.KEYDOWN:
                if audio:
                    videoFlag.clear()
                return True

            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     x, y = pg.mouse.get_pos()
            #     rgb = img[y, x]
            #     result.append({'time': t, 'position': (x, y),
            #                    'color': rgb})
            #     print("time, position, color : ", "%.03f, %s, %s" %
            #           (t, str((x, y)), str(rgb)))

        t1 = time.time()
        time.sleep(max(0, t - (t1 - t0)))
        imdisplay(img, screen, position)


def play_video_loop(filename, screen, duration=-1):
    clip = VideoFileClip(filename)
    if duration == -1:
        # infinite loop until key press
        stop = False
        while not stop:
            stop = play_video(clip, screen)
    else:
        # loop until total duration or key press
        start = pg.time.get_ticks()
        stop = False
        while not stop and pg.time.get_ticks() - start <= duration:
            stop = play_video(clip, screen)


def play_two_videos(clip1, clip2, screen, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000,
            audio_nbytes=2):

    # get clip size
    size = clip1.size
    # get screen size
    display_info = pg.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    position1 = (0, int((screen_height - size[1]) / 2))
    position2 = (int(screen_width - size[0]), int((screen_height - size[1]) / 2))

    audio = audio and (clip1.audio is not None)

    if audio:
        # the sound will be played in parrallel. We are not
        # parralellizing it on different CPUs because it seems that
        # pygame and openCV already use several cpus it seems.

        # two synchro-flags to tell whether audio and video are ready
        videoFlag = threading.Event()
        audioFlag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(target=clip1.audio.preview,
                                       args=(audio_fps,
                                             audio_buffersize,
                                             audio_nbytes,
                                             audioFlag, videoFlag))
        audiothread.start()

    img1 = clip1.get_frame(0)
    img2 = clip2.get_frame(0)
    imdisplay(img1, screen, position1)
    imdisplay(img2, screen, position2)
    if audio:  # synchronize with audio
        videoFlag.set()  # say to the audio: video is ready
        audioFlag.wait()  # wait for the audio to be ready

    result = []

    t0 = time.time()
    for t in np.arange(1.0 / fps, clip1.duration - .001, 1.0 / fps):

        img1 = clip1.get_frame(t)
        img2 = clip2.get_frame(t)

        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if audio:
                    videoFlag.clear()
                print("Interrupt")
                return True
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if audio:
                    videoFlag.clear()
                return True

            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     x, y = pg.mouse.get_pos()
            #     rgb = img[y, x]
            #     result.append({'time': t, 'position': (x, y),
            #                    'color': rgb})
            #     print("time, position, color : ", "%.03f, %s, %s" %
            #           (t, str((x, y)), str(rgb)))

        t1 = time.time()
        time.sleep(max(0, t - (t1 - t0)))
        imdisplay(img1, screen, position1)
        imdisplay(img2, screen, position2)


def play_two_videos_loop(filename1, filename2, screen, duration=-1, audio=True):
    clip1 = VideoFileClip(filename1)
    clip2 = VideoFileClip(filename2)

    if duration == -1:
        # play video with keyboard interruption
        stop = False
        while not stop:
            stop = play_two_videos(clip1, clip2, screen, audio=audio)
    else:
        # Play video without interruption
        start = pg.time.get_ticks()
        while pg.time.get_ticks() - start <= duration:
            play_two_videos(clip1, clip2, screen, audio=audio)


def play_video_2s(clip, screen, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000,
            audio_nbytes=2, fullscreen=False):
    """
    Displays the clip in a window, at the given frames per second
    (of movie) rate. It will avoid that the clip be played faster
    than normal, but it cannot avoid the clip to be played slower
    than normal if the computations are complex. In this case, try
    reducing the ``fps``.

    Parameters
    ------------

    fps
      Number of frames per seconds in the displayed video.

    audio
      ``True`` (default) if you want the clip's audio be played during
      the preview.

    audio_fps
      The frames per second to use when generating the audio sound.

    fullscreen
      ``True`` if you want the preview to be displayed fullscreen.

    """
    # Center video on the screen
    # get clip size
    size = clip.size
    # get screen size
    display_info = pg.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    position = (int((screen_width - size[0]) / 2), int((screen_height - size[1]) / 2))

    if fullscreen:
        flags = pg.FULLSCREEN
    else:
        flags = 0

    # compute and splash the first image
    # screen = pg.display.set_mode(clip.size, flags)

    audio = audio and (clip.audio is not None)

    if audio:
        # the sound will be played in parrallel. We are not
        # parralellizing it on different CPUs because it seems that
        # pygame and openCV already use several cpus it seems.

        # two synchro-flags to tell whether audio and video are ready
        videoFlag = threading.Event()
        audioFlag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(target=clip.audio.preview,
                                       args=(audio_fps,
                                             audio_buffersize,
                                             audio_nbytes,
                                             audioFlag, videoFlag))
        audiothread.start()

    img = clip.get_frame(0)
    imdisplay(img, screen, position)
    if audio:  # synchronize with audio
        videoFlag.set()  # say to the audio: video is ready
        audioFlag.wait()  # wait for the audio to be ready

    result = []

    t0 = time.time()
    video_start = pg.time.get_ticks()
    for t in np.arange(1.0 / fps, clip.duration - .001, 1.0 / fps):
        video_now = pg.time.get_ticks()
        if video_now - video_start >= 2500:
            if audio:
                videoFlag.clear()
            return "no_key"

        img = clip.get_frame(t)

        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if audio:
                    videoFlag.clear()
                print("Interrupt")
                return "Interrupt"
            # elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            elif event.type == pg.KEYDOWN:
                video_start = pg.time.get_ticks()


                # if audio:
                #     videoFlag.clear()
                # return True

            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     x, y = pg.mouse.get_pos()
            #     rgb = img[y, x]
            #     result.append({'time': t, 'position': (x, y),
            #                    'color': rgb})
            #     print("time, position, color : ", "%.03f, %s, %s" %
            #           (t, str((x, y)), str(rgb)))

        t1 = time.time()
        time.sleep(max(0, t - (t1 - t0)))
        imdisplay(img, screen, position)
    return "stimulus"


def play_video_loop_p3test(filename, screen, duration=-1):
    clip = VideoFileClip(filename)
    if duration == -1:
        # infinite loop until key press
        stop = False
        while not stop:
            stop = play_video(clip, screen)
            return "keypress"
        return "stimulus"
    else:
        # loop until total duration or key press
        start = pg.time.get_ticks()
        stop = False
        while not stop and pg.time.get_ticks() - start <= duration:
            stop = play_video(clip, screen)


def play_two_videos_audio(clip1, clip2, audioside, screen, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000,
            audio_nbytes=2):

    # get clip size
    size = clip1.size
    # get screen size
    display_info = pg.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    position1 = (0, int((screen_height - size[1]) / 2))
    position2 = (int(screen_width - size[0]), int((screen_height - size[1]) / 2))

    if audioside == "left":
        audioclip = clip1
    elif audioside == "right":
        audioclip = clip2

    audio = audio and (audioclip.audio is not None)

    if audio:
        # the sound will be played in parrallel. We are not
        # parralellizing it on different CPUs because it seems that
        # pygame and openCV already use several cpus it seems.

        # two synchro-flags to tell whether audio and video are ready
        videoFlag = threading.Event()
        audioFlag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(target=audioclip.audio.preview,
                                       args=(audio_fps,
                                             audio_buffersize,
                                             audio_nbytes,
                                             audioFlag, videoFlag))
        audiothread.start()

    img1 = clip1.get_frame(0)
    img2 = clip2.get_frame(0)
    imdisplay(img1, screen, position1)
    imdisplay(img2, screen, position2)
    if audio:  # synchronize with audio
        videoFlag.set()  # say to the audio: video is ready
        audioFlag.wait()  # wait for the audio to be ready

    result = []

    t0 = time.time()
    for t in np.arange(1.0 / fps, clip1.duration - .001, 1.0 / fps):

        img1 = clip1.get_frame(t)
        img2 = clip2.get_frame(t)

        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if audio:
                    videoFlag.clear()
                print("Interrupt")
                return True
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if audio:
                    videoFlag.clear()
                return True

            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     x, y = pg.mouse.get_pos()
            #     rgb = img[y, x]
            #     result.append({'time': t, 'position': (x, y),
            #                    'color': rgb})
            #     print("time, position, color : ", "%.03f, %s, %s" %
            #           (t, str((x, y)), str(rgb)))

        t1 = time.time()
        time.sleep(max(0, t - (t1 - t0)))
        imdisplay(img1, screen, position1)
        imdisplay(img2, screen, position2)