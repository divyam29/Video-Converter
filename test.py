# importing the module
import cv2

# reading the video
print(f'\nHello\n')
source = cv2.VideoCapture(f'static/uploads/sample1.mp4')
height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
size = (width, height)
down_size = (int(width/2), int(height/2))
fps = source.get(cv2.CAP_PROP_FPS)
print()
print(height, width, size, down_size, fps)
print()
result = cv2.VideoWriter(
    f'static/modified/sample1.mp4',
    cv2.VideoWriter_fourcc(*'XVID'),
    fps,
    down_size,
    0
)

# running the loop
while True:
    # extracting the frames
    ret, img = source.read()
    if ret == True:
        # converting to gray-scale
        img2=cv2.resize(img,down_size,fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        result.write(gray)
        # displaying the video
        cv2.imshow("Live", gray)

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
