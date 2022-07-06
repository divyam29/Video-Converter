# Import everything needed to edit video clips
from moviepy.editor import *

# loading video dsa gfg intro video
# and getting only first 5 seconds
clip1 = VideoFileClip("static/uploads/Papa_50th_Bday.mp4")

# getting width and height of clip 1
w1 = clip1.w
h1 = clip1.h

print("Width x Height of clip 1 : ", end=" ")
print(str(w1) + " x ", str(h1))

print("---------------------------------------")

# resizing video downsize 50 %
clip2 = clip1.resize(0.5)
clip3 = clip2.fx(vfx.blackwhite, RGB=None, preserve_luminosity=True)
# getting width and height of clip 1
w2 = clip3.w
h2 = clip3.h

print("Width x Height of clip 2 : ", end=" ")
print(str(w2) + " x ", str(h2))

print("---------------------------------------")

# showing final clip
clip3.write_videofile("static/modified/Papa_50th_Bday.mp4")