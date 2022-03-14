# importing the libraries
import cv2
import mediapipe as media_pipe
from controls import *
import threading

# Intiallizations of variables from opencv, mediapipe

# 1.Opencv reading the live web cam feed
video_capture = cv2.VideoCapture(0)

# 2. Media pipe - Using drawing_utils and pose modules in media pipe, I am initializing the pose
media_pipe_solutions = media_pipe.solutions
media_pipe_drawing = media_pipe_solutions.drawing_utils
media_pipe_pose = media_pipe_solutions.pose
i = 50

with media_pipe_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    # using cv I have opened the vedio capture, so that pose can be detectecd in future steps
    while video_capture.isOpened():
        # intiallizing the action to empty string
        action = ""

        # intiallizing the shoulders midpoint
        shoulders_midpoint = ('0', '0')

        # video which is captured from cam-feed using open cv is read here
        _, frame = video_capture.read()
        # coloring the image to from BGR to RGB format using a opencv2 module COLOR_BGR2RGB
        input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # setting writeable flags to false, this is for intallization purpose
        input_image.flags.writeable = False
        # detecting the pose from the input image.
        results = pose.process(input_image)
        input_image.flags.writeable = True
        # recoloring the input_image from RGB to BGR using a opencv2 module COLOR_RGB2BGR
        input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)

        # added try block to handle the errors through the expection block
        try:
            # intiallizing the thresholds for implementing box rectangles
            right_threshold = 400
            left_threshold = 550
            top_threshold = 400

            # reading the pose landmarks from the results
            result_pose_land_marks = results.pose_landmarks.landmark
            mediapipe_pose_land_marks_left_shoulder = media_pipe_pose.PoseLandmark.LEFT_SHOULDER.value
            mediapipe_pose_land_marks_right_shoulder = media_pipe_pose.PoseLandmark.RIGHT_SHOULDER.value
            # intiallizing the left shoulder and right shoulder with 0
            left_shoulder = [0, 0]
            right_shoulder = [0, 0]

            # reading points of left part of shoulder using media
            left_shoulder[0] = result_pose_land_marks[mediapipe_pose_land_marks_left_shoulder].x
            left_shoulder[1] = result_pose_land_marks[mediapipe_pose_land_marks_left_shoulder].y

            # reading points of right part of shoulder using media
            right_shoulder[0] = result_pose_land_marks[mediapipe_pose_land_marks_right_shoulder].x
            right_shoulder[1] = result_pose_land_marks[mediapipe_pose_land_marks_right_shoulder].y

            # calculating midpoint of the shoulders using left shoulder and right shoulder points from media pipe
            # print(left_shoulder, right_shoulder)
            # multiplying the shoulders value with multiple of 10 as media pipe is giving the points between 0 to 1
            shoulders_midpoint = [int((left_shoulder[0] * 1000 + right_shoulder[0] * 1000) // 2),
                                     int((left_shoulder[1] * 1000 + right_shoulder[1] * 1000) // 2)]

            if shoulders_midpoint[0] < int(right_threshold) and shoulders_midpoint[1] > int(
                    top_threshold):
                action = 'Right' + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])
                t_right = threading.Thread(target=move_right)
                t_right.start()
            elif shoulders_midpoint[0] > left_threshold and shoulders_midpoint[1] > top_threshold:
                action = 'Left' + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])
                t_left = threading.Thread(target=move_left)
                t_left.start()
            elif shoulders_midpoint[1] < top_threshold:
                if shoulders_midpoint[0] < right_threshold:
                    action = "Right jump" + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])
                    jump_right()
                elif shoulders_midpoint[0] > left_threshold:
                    action = "Left jump" + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])
                    jump_left()
                else:
                    action = "Jump " + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])
                    jump()
            else:
                do_nothing()
                action = "Do Nothing " + str(shoulders_midpoint[0]) + ', ' + str(shoulders_midpoint[1])

        except Exception as e:
            print("enter exception", e)

        # drawing the landmarks on the image using media pipe
        media_pipe_drawing.draw_landmarks(input_image,
                                          results.pose_landmarks,
                                          media_pipe_pose.POSE_CONNECTIONS,
                                          media_pipe_drawing.DrawingSpec(color=(255,99,71), thickness=4, circle_radius=3),
                                          media_pipe_drawing.DrawingSpec(color=(178,34,34), thickness=4, circle_radius=3)
                                  )

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (100, 200)
        fontScale = 4
        color = (255, 69, 0)
        thickness = 7

        # writing the action on image for decode purpose
        input_image = cv2.putText(input_image, action, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

        cv2.imshow('Cam Feed', input_image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # stop vedio capture and detroy the cam feed window
    video_capture.release()
    cv2.destroyAllWindows()