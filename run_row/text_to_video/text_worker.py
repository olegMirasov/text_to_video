from math import ceil

from .settings import TEMP_VIDEO_PATH, VIDEO_FPS
from pygame import font, Surface, surfarray
import pygame as pg
import cv2
import datetime
pg.init()

PATH = TEMP_VIDEO_PATH
FPS = VIDEO_FPS

FORMAT = '.mp4'

all_formats = {'.mp4': 'mp4v'}  # we can add other
codec = all_formats[FORMAT]
fourcc = cv2.VideoWriter.fourcc(*codec)


class __Counter:
    __id = 0
    __max_id = 10 ** 5

    @classmethod
    def get(cls) -> str:
        temp = cls.__id
        cls.__id += 1
        if cls.__id >= cls.__max_id:
            cls.__id = 0

        video_name = f'{datetime.datetime.now().date()}_{temp}{FORMAT}'

        return f'{PATH}{video_name}'


def text_to_video(text: str,
                  size: tuple = (100, 100),
                  color: tuple = (255, 255, 255),
                  bg_color: tuple = (0, 0, 0),
                  time_: int | float = 3.0,
                  use_font: str | None = None) -> dict:
    """

    :param text:
    :param size:
    :param color:
    :param bg_color:
    :param time_: video len
    :param use_font: not work now, adding future
    :return: path to video file
    """
    # META
    __fps = FPS

    # delete before debuging
    color = color[::-1]
    if bg_color:
        bg_color = bg_color[::-1]

    # create data for db
    video_data = {'text': text,
                  'size': size,
                  'color': color,
                  'bg_color': bg_color,
                  'video_len': time_}

    # create a full image from text
    my_font = pg.font.Font(use_font, size=size[-1])
    full_image = my_font.render(text, True, color)

    # resize image
    full_image = pg.transform.rotozoom(full_image, 0, size[-1] / full_image.get_height())

    # find the offset based on the time of the video and the length of the text
    image_w = full_image.get_width()
    all_length = image_w + 2 * size[0]
    count_images = ceil(__fps * time_)
    offset = int(all_length / count_images)

    # create image strip to video
    images = []
    start_x = size[0]
    for i in range(count_images):
        temp = pg.Surface(size)
        temp.fill(bg_color)
        temp.blit(full_image, (start_x - offset * i, 0))
        temp = pg.transform.rotate(temp, 90)
        temp = pg.transform.flip(temp, 0, 1)
        images.append(temp)

    # create video
    path = __Counter.get()
    video = cv2.VideoWriter(path, fourcc, __fps, size)
    for i in images:
        temp = pg.surfarray.array3d(i)
        video.write(temp)
    video.release()

    return {'video_path': path, 'video_data': video_data}
