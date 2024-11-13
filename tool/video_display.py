# frontend/video_display.py

import cv2

def display_frame(cap, frame_idx, results):
    """Displays a specific frame with tracked objects."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    
    if ret:
        for obj in results[frame_idx]:
            box = obj["boxes"]
            track_id = obj["track_id"]
            class_id = obj["class_id"]
            confidence = obj["confidence"]

            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"ID: {track_id}, Class: {class_id}, Conf: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.putText(frame, f"Frame: {frame_idx}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Tracking Results', frame)
        return True
    return False
