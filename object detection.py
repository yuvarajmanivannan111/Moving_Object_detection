

import cv2
import imutils

cam = cv2.VideoCapture(0)

firstframe = None
area = 500

while True:
    # Capture frame-by-frame
    _, img = cam.read()
    text = "STABLE"
    # Resize the image
    img = imutils.resize(img, width=500)

    # Convert to grayscale
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    #gaussianimg= cv2.GaussianBlur(src,(kernel),bordertype)
    gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)

    # Initialize the first frame
    if firstframe is None:
        firstframe = gaussianImg
        continue

    # Compute the absolute difference between the current frame and first frame
    imgDiff = cv2.absdiff(firstframe, gaussianImg)
    threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    threshImg = cv2.dilate(threshImg, None, iterations=2)

    # Find contours
    cnts, _ = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for c in cnts:
        if cv2.contourArea(c) < area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "OBJECT IS MOVING"

    # Display the text
    cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("camerafeed", img)

    # Break the loop on 'q' key press
    key = cv2.waitKey(10)
    if key == ord("q"):
        break

# Release the camera and destroy all windows
cam.release()
cv2.destroyAllWindows()






    
