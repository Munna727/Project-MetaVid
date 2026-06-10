import io
import os
import uuid
import cv2
import cloudinary
import cloudinary.uploader
from google.cloud import videointelligence_v1 as videointelligence


# ==============================
# 1️⃣ Detect Objects
# ==============================

def object_tracker(path):
    client = videointelligence.VideoIntelligenceServiceClient()

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = client.annotate_video(
        request={
            "features": [videointelligence.Feature.OBJECT_TRACKING],
            "input_content": input_content
        }
    )

    result = operation.result(timeout=600)

    return result.annotation_results[0].object_annotations


# ==============================
# 2️⃣ Extract Cropped Objects + JSON
# ==============================

def extract_objects_and_generate_json(object_annotations, input_path, video_id):

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise Exception("Error opening video file")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    enriched_data = {
        "video_id": video_id,
        "objects": []
    }

    for annotation in object_annotations:

        label = annotation.entity.description
        frames = annotation.frames

        if not frames:
            continue

        # Pick middle frame for stable representative
        best_frame = frames[len(frames) // 2]

        time_offset = (
            best_frame.time_offset.seconds +
            best_frame.time_offset.microseconds / 1e6
        )

        # Jump to that timestamp
        cap.set(cv2.CAP_PROP_POS_MSEC, time_offset * 1000)
        success, frame = cap.read()

        if not success:
            continue

        box = best_frame.normalized_bounding_box

        x1 = max(0, int(box.left * width))
        y1 = max(0, int(box.top * height))
        x2 = min(width, int(box.right * width))
        y2 = min(height, int(box.bottom * height))

        if x2 <= x1 or y2 <= y1:
            continue

        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            continue

        unique_name = f"{video_id}_{uuid.uuid4().hex}.jpg"
        cv2.imwrite(unique_name, crop)

        try:
            upload_result = cloudinary.uploader.upload(
                unique_name,
                folder=f"metavid_objects/{video_id}",
                resource_type="image"
            )

            image_url = upload_result.get("secure_url")

        except Exception as e:
            print("Cloudinary upload failed:", e)
            os.remove(unique_name)
            continue

        os.remove(unique_name)

        enriched_data["objects"].append({
            "name": label,
            "timestamp": round(time_offset, 2),
            "image_url": image_url
        })

    cap.release()

    return enriched_data


# ==============================
# 3️⃣ Draw Bounding Boxes
# ==============================

def draw_object_box(frame, normalized_box, label, color=(0, 255, 0)):

    h, w, _ = frame.shape

    left = int(normalized_box.left * w)
    top = int(normalized_box.top * h)
    right = int(normalized_box.right * w)
    bottom = int(normalized_box.bottom * h)

    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    text_size, _ = cv2.getTextSize(
        label,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        2
    )

    text_w, text_h = text_size

    cv2.rectangle(
        frame,
        (left, top - text_h - 10),
        (left + text_w + 6, top),
        color,
        -1
    )

    cv2.putText(
        frame,
        label,
        (left + 3, top - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        2
    )

    return frame


# ==============================
# 4️⃣ Annotate Video
# ==============================

def annotate_video_with_object_tracking(
        input_video_path,
        output_video_path,
        object_annotations
):

    print("Bounding boxes started...")

    cap = cv2.VideoCapture(input_video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_index / fps

        for obj in object_annotations:

            label = obj.entity.description

            for obj_frame in obj.frames:

                frame_time = (
                    obj_frame.time_offset.seconds +
                    obj_frame.time_offset.microseconds / 1e6
                )

                if abs(frame_time - current_time) < (1 / fps):

                    frame = draw_object_box(
                        frame,
                        obj_frame.normalized_bounding_box,
                        label
                    )

        out.write(frame)
        frame_index += 1

    cap.release()
    out.release()

    print("Bounding boxes completed.")
