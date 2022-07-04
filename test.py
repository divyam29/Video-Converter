# importing the module
import cv2
import magic

# printing the human readable type of the file
print(magic.from_file('static/uploads/sample.mp4'))
# printing the mime type of the file
print(magic.from_file('static/uploads/sample.mp4', mime=True))

# reading the video
source = cv2.VideoCapture('static/uploads/sample.mp4')
height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
size = (width, height)
fps = source.get(cv2.CAP_PROP_FPS)
print()
print(height, width, size, fps)
print()
result = cv2.VideoWriter(
    'static/modified/sample_modified.mp4',
    cv2.VideoWriter_fourcc(*'XVID'),
    fps,
    size,
    0
)
# running the loop
while True:
    
        # extracting the frames
    ret, img = source.read()
    if ret == True:
        # converting to gray-scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result.write(gray)
        # displaying the video
        # cv2.imshow("Live", gray)

        # exiting the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    else:
        break

# closing the window
cv2.destroyAllWindows()
source.release()
result.release()
