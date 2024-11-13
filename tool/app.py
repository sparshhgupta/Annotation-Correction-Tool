# backend/app.py

import pandas as pd

def retrieve_tracking_results(csv_path='tracking_results.csv'):
    """Reads the tracking results CSV and structures it by frame."""
    df = pd.read_csv(csv_path)
    results_by_frame = {}
    
    for _, row in df.iterrows():
        frame_idx = int(row['frame'])
        detection = {
            "track_id": int(row['track_id']),
            "class_id": int(row['class_id']),
            "confidence": float(row['confidence']),
            "boxes": [float(row['x1']), float(row['y1']), float(row['x2']), float(row['y2'])]
        }
        if frame_idx not in results_by_frame:
            results_by_frame[frame_idx] = []
        results_by_frame[frame_idx].append(detection)
    
    max_frame = max(results_by_frame.keys()) + 1
    results = [results_by_frame.get(frame_idx, []) for frame_idx in range(max_frame)]
    print("Tracking results successfully loaded from", csv_path)
    return results

def save_tracking_results_to_csv(results, output_path='updated_tracking_results.csv'):
    """Saves the tracking results into a CSV file."""
    frame_numbers = []
    track_ids = []
    classes = []
    confidences = []
    x1_coords = []
    y1_coords = []
    x2_coords = []
    y2_coords = []

    for frame_idx, frame_results in enumerate(results):
        for obj in frame_results:
            frame_numbers.append(frame_idx)
            track_ids.append(obj["track_id"])
            classes.append(obj["class_id"])
            confidences.append(obj["confidence"])
            x1_coords.append(obj["boxes"][0])
            y1_coords.append(obj["boxes"][1])
            x2_coords.append(obj["boxes"][2])
            y2_coords.append(obj["boxes"][3])

    df = pd.DataFrame({
        'frame': frame_numbers,
        'track_id': track_ids,
        'class_id': classes,
        'confidence': confidences,
        'x1': x1_coords,
        'y1': y1_coords,
        'x2': x2_coords,
        'y2': y2_coords
    })
    df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
