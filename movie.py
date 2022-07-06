# Import everything needed to edit video clips
from moviepy.editor import *

def edit_video(filename):
    clip1 = VideoFileClip(f'static/uploads/{filename}')

    clip2 = clip1.resize(0.5)
    clip3 = clip2.fx(vfx.blackwhite, RGB=None, preserve_luminosity=True)

    clip3.write_videofile(f"static/modified/{filename}")