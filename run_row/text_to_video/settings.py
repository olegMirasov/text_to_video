
from pathlib import Path

# VIDEO SETTINGS

metadata = {'app_name': 'text_to_video',
            'temp_video': 'temp_video'}

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_FPS = 30
TEMP_VIDEO_PATH = BASE_DIR.joinpath(Path(f'{metadata["app_name"]}/{metadata["temp_video"]}'))

MAX_LEN = 50            # len text
MAX_SIZE = 400          # pixels
MAX_COL = 255           # for color
MAX_TIME = 20           # video len, seconds
