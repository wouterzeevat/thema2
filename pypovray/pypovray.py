"""
This module offers functionality to render a frame or movie given a
Vapory 'Scene' object.
"""

import shutil
import sys
import os
from tempfile import mkdtemp
from glob import glob
from distutils import util
from math import ceil
from moviepy.editor import ImageSequenceClip
from pathos.multiprocessing import ProcessingPool as Pool
import ffmpy
from pypovray import SETTINGS, logger


def render_scene_to_png(frame, frame_id=0):
    """ Renders one or more frames given the `frame` function object and  a
    frame number (int, list or range) which is passed to the `frame` function """
    tmp_folder = _create_tmp_folder()

    if isinstance(frame_id, int):
        if frame_id < 0 or frame_id > eval(SETTINGS.NumberFrames):
            logger.warning('["%s"] - Frame number(s) outside of range(0, %d)',
                           sys._getframe().f_code.co_name, eval(SETTINGS.NumberFrames))
        _render_frame(frame(frame_id), frame_id)

    elif isinstance(frame_id, (list, range)):
        if min(frame_id) < 0 or max(frame_id) > eval(SETTINGS.NumberFrames):
            logger.warning('["%s"] - Frame number(s) outside of range(0, %d)',
                           sys._getframe().f_code.co_name, eval(SETTINGS.NumberFrames))

        for id in frame_id:
            _render_frame(frame(id), id)
    else:
        logger.error('["%s"] - Not simulating; given frame number(s) not of integer or list type.',
                     sys._getframe().f_code.co_name)
        return

    # Remove temporary files after rendering, if set
    if SETTINGS.LogLevel != "DEBUG" or util.strtobool(SETTINGS.RemoveTempFiles):
        shutil.rmtree(tmp_folder)


def render_scene_to_gif(scene, frame_ids=None):
    """ Creates a GIF output 'movie' using moviepy.
    NOTE: a GIF file has reduced quality compared to the rendered output!
    """

    if _check_output_file_exists("gif"):
        logger.error('["%s"] - Not simulating; output file already exists.',
                     sys._getframe().f_code.co_name)
        return

    if _check_rendered_images():
        logger.error('["%s"] - Not simulating; output image file(s) already exist.',
                     sys._getframe().f_code.co_name)
        return

    # Render the scenes (creates PNG images in the SETTINGS.OutputImageDir folder)
    _render_scene(scene, frame_ids)

    # Get a list of all rendered images (these are ordered by default)
    image_files = glob('{}/{}_*.png'.format(SETTINGS.OutputImageDir, SETTINGS.OutputPrefix))
    # Combine images into GIF file using moviepy
    ImageSequenceClip(sorted(image_files),
                      fps=SETTINGS.RenderFPS).write_gif('{}/{}.gif'.format(SETTINGS.OutputMovieDir,
                                                                           SETTINGS.OutputPrefix))


def render_scene_to_mp4(scene, frame_ids=None):
    """ Creates an MP4 movie using 'ffmpeg' from n > 1 rendered images"""

    if _check_output_file_exists("mp4"):
        logger.error('["%s"] - Not simulating; output mp4 file already exists.',
                     sys._getframe().f_code.co_name)
        return

    if _check_rendered_images():
        logger.error('["%s"] - Not simulating; output image file(s) already exist.',
                     sys._getframe().f_code.co_name)
        return

    # Render the scenes (creates PNG images in the SETTINGS.OutputImageDir folder)
    _render_scene(scene, frame_ids)

    # Combine the frames into a movie
    _run_ffmpeg()


def _render_scene(scene, frame_ids=None):
    """ Renders the scene to multiple output PNG files for use in animations """

    # Clear 'images' folder containing previously rendered frames
    _remove_folder_contents(SETTINGS.OutputImageDir)

    # Calculate the time per frame (i.e. evaluate expression from config file)
    if frame_ids:
        logger.debug('["%s"] - Specific frames given, rendering part of the simulation..',
                     sys._getframe().f_code.co_name)
        nframes = len(frame_ids)
        id_list = frame_ids
    else:
        logger.debug('["%s"] - No specific frames given, rendering complete simulation..',
                     sys._getframe().f_code.co_name)
        nframes = ceil(eval(SETTINGS.NumberFrames))
        id_list = range(nframes)

    # Render each scene using a thread pool or single-threaded
    if util.strtobool(SETTINGS.UsePool):
        scene_flist = [scene] * nframes

        # Render each scene, using a thread pool
        with Pool(int(SETTINGS.workers)) as p:
            p.map(render_scene_to_png, scene_flist, id_list)

    else:
        for frame_id in id_list:
            render_scene_to_png(scene, frame_id)


def _remove_folder_contents(folder, match=None):
    """ Cleans up folder contents """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                if match:
                    if match in the_file:
                        os.unlink(file_path)
                else:
                    os.unlink(file_path)
        except Exception as e:
            print(e)


def _render_frame(scene, frame_id):
    """ Renders a single frame """
    #logger.debug("Step %d, in seconds: %f.", frame_id, frame_id / eval(SETTINGS.NumberFrames))
    frame_file = _create_frame_file_name(frame_id)
    scene.render(frame_file,
                 width=SETTINGS.ImageWidth,
                 height=SETTINGS.ImageHeight,
                 antialiasing=SETTINGS.AntiAlias,
                 show_window=util.strtobool(SETTINGS.ShowWindow),
                 quality=SETTINGS.Quality,
                 remove_temp=util.strtobool(SETTINGS.RemoveTempFiles))


def _create_tmp_folder():
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)
    logger.debug('["%s"] - tmp_folder: %s', sys._getframe().f_code.co_name, tmp_folder)
    return tmp_folder


def _create_frame_file_name(frame):
    output_file = '{}/{}_{}.png'.format(SETTINGS.OutputImageDir,
                                        SETTINGS.OutputPrefix, str(round(frame, 2)).zfill(3))
    logger.debug('["%s"] - output file: %s', sys._getframe().f_code.co_name, output_file)
    return output_file


def _check_output_file_exists(extension):
    """ Informs about existing output file before creating a new one
    and offers to overwrite the existing file. """
    output_file = '{}/{}.{}'.format(SETTINGS.OutputMovieDir,
                                    SETTINGS.OutputPrefix, extension)
    remove_file = "n"
    if os.path.exists(output_file):
        remove_file = str(input("The file '%s' already exists, do you want to overwrite? (y/n): " % output_file))
    if remove_file.lower() == "y":
        os.remove(output_file)

    return os.path.exists(output_file)


def _check_rendered_images():
    """ Informs about existing output image files before rendering
    and offers to overwrite the existing file. """
    remove_files = "n"
    if os.listdir(SETTINGS.OutputImageDir):
        if any(SETTINGS.OutputPrefix in fname for fname in os.listdir(SETTINGS.OutputImageDir)):
            remove_files = str(input("Image files already exists in %s, " % SETTINGS.OutputImageDir +
                                     "do you want to overwrite? (y/n): "))
    if remove_files.lower() == "y":
        _remove_folder_contents(SETTINGS.OutputImageDir, match=SETTINGS.OutputPrefix)

    return any(SETTINGS.OutputPrefix in fname for fname in os.listdir(SETTINGS.OutputImageDir))


def _run_ffmpeg():
    """ Builds the ffmpeg command to render an MP4 movie file using the
    h.x264 codex and yuv420p format """
    ff = ffmpy.FFmpeg(
        # Input is a pattern for all image files ordered by number (padded)
        inputs={'': '-framerate {} -pattern_type glob -i {}/{}_*.png'.format(
            SETTINGS.RenderFPS,
            SETTINGS.OutputImageDir,
            SETTINGS.OutputPrefix)},
        outputs={'{}/{}.mp4'.format(SETTINGS.OutputMovieDir,
                                    SETTINGS.OutputPrefix):
                     '-c:v libx264 -r {} -crf 2 -pix_fmt yuv420p -loglevel warning'.format(SETTINGS.MovieFPS)}
    )
    # Run ffmpeg and create output movie file
    logger.info('["%s"] - ffmpeg command: "%s"', sys._getframe().f_code.co_name, ff.cmd)
    ff.run()
