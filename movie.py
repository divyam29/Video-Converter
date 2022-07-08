# Import everything needed to edit video clips
from moviepy.editor import *
import cv2

def edit_video(filename,resize,grayscale):
    source = cv2.VideoCapture(f'static/uploads/{filename}')
    height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    size = (height, width)
    clip = VideoFileClip(f'static/uploads/{filename}',target_resolution=size)
    clip_fps=clip.fps
    print(clip_fps)
    clip = clip.resize(3)
    if resize:
        clip = clip.resize(0.5)
    if grayscale:
        clip = clip.fx(vfx.blackwhite, RGB=None, preserve_luminosity=True)

    if resize and grayscale:
        modifed_file=f'static/modified/resized-grayscaled-{filename}'
    elif resize:
        modifed_file=f'static/modified/resized-{filename}'
    elif grayscale:
        modifed_file=f'static/modified/grayscaled-{filename}'
    else:
        modifed_file=f'static/modified/{filename}'
    
    clip.write_videofile(modifed_file,fps=clip_fps)
    return modifed_file