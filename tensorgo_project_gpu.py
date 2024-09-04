"""
written by NAGA DEEPIKA NIMMAKAYALA
"""


import cv2
import easyocr
import time
from google.colab.patches import cv2_imshow


reader = easyocr.Reader(['en'], gpu=True)

video_path = '/demo.mp4'
cap = cv2.VideoCapture(video_path)

frame_count = 0
total_time = 0
accurate_detections = 0
total_detections = 0


if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")
else:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        start_time = time.time()


        result = reader.readtext(frame)


        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        frame_count += 1


        for (bbox, text, prob) in result:

            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            frame = cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            frame = cv2.putText(frame, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)


            if prob > 0.8:
                accurate_detections += 1
            total_detections += 1


        if total_time > 0:
            fps = frame_count / total_time
        else:
            fps = 0

        frame = cv2.putText(frame, f'FPS: {fps:.2f}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


        if total_detections > 0:
            accuracy = (accurate_detections / total_detections) * 100
        else:
            accuracy = 0
        frame = cv2.putText(frame, f'Accuracy: {accuracy:.2f}%', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


        cv2_imshow(frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()


    if frame_count > 0:
        print(f'Total Frames: {frame_count}')
        print(f'Average FPS: {fps:.2f}')
        print(f'Overall Accuracy: {accuracy:.2f}%')
    else:
        print("No frames processed. Check if the video file is correct and accessible.")