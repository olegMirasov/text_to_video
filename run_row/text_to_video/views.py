from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse

from .settings import MAX_SIZE, MAX_COL, MAX_LEN, MAX_TIME
from .text_worker import text_to_video, description
from .models import History

import os


_names = 'text size color bg_color time_'.split()
_labels = ['Текст', "Размер", "Цвет текста", "Цвет фона", "Длина ролика"]
_placeholders = ['IT solution', '100,100', '15,251,78', '78,25,158', '5']

form_data = []
for n, l, p in zip(_names, _labels, _placeholders):
    temp = {'name': n, 'label': l, 'place': p}
    form_data.append(temp)

use_data = {'data': form_data, 'description': description}


def __tuple_for_video(text: str, count: int, mi: int = 0, ma: int = 255) -> tuple | None:
    if not text:
        return None

    try:
        result = [int(i) for i in text.split(',')]
        if len(result) != count:
            raise Exception()
        result = [min(ma, max(mi, i)) for i in result]
        result = tuple(result)

    except Exception:
        result = None

    return result


def _prepare_data(data: dict) -> dict:
    """
    a temporary function for health check
    :param data: data from form
    :return: dict for text_to_video function
    """
    my_dict = {}

    text = data['text']
    text = text[:MAX_LEN] if text else ' '

    size = __tuple_for_video(text=data['size'], count=2, mi=10, ma=MAX_SIZE)
    color = __tuple_for_video(text=data['color'], count=3, ma=MAX_COL)
    bg_color = __tuple_for_video(text=data['bg_color'], count=3, ma=MAX_COL)
    time_ = __tuple_for_video(data['time_'], count=1, ma=MAX_TIME)
    if time_:
        time_ = time_[0]

    for k, v in zip(_names, [text, size, color, bg_color, time_]):
        if v:
            my_dict[k] = v

    return my_dict


def _add_history(data: dict) -> None:
    History.objects.create(**data)


def index(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'text_to_video/index.html', use_data)

    # prepare data for creating video
    data_for_video = _prepare_data(request.POST)
    video_params = text_to_video(**data_for_video)
    with open(video_params['video_path'], "rb") as f:
        file = f.read()
    response = HttpResponse(file, content_type='video/mp4')
    response['Content-Disposition'] = "attachment; filename=my_video.mp4"

    # add data to db
    _add_history(data=video_params['video_data'])

    # clean temp files
    os.remove(video_params['video_path'])

    return response
