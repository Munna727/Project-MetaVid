import cloudinary
import cloudinary.uploader
import os
import json
import io
import cv2
import subprocess
import uuid
from google.cloud import videointelligence_v1 as videointelligence

# FFMPEG_PATH = (
#     r"C:\Users\Akshay\AppData\Local\Microsoft\WinGet\Packages"
#     r"\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe"
#     r"\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
# )
FFMPEG_PATH = r"C:\Users\MEGHANA\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
# cloudinary.config(
#     cloud_name="YOUR_CLOUD_NAME",
#     api_key="YOUR_API_KEY",
#     api_secret="YOUR_API_SECRET",
# )




def detect_faces(input_path):
    """Run Google Video Intelligence face detection."""
    client = videointelligence.VideoIntelligenceServiceClient()

    with io.open(input_path, "rb") as f:
        input_content = f.read()

    config = videointelligence.FaceDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=True,
    )

    context = videointelligence.VideoContext(
        face_detection_config=config
    )

    operation = client.annotate_video(
        request={
            "features": [videointelligence.Feature.FACE_DETECTION],
            "input_content": input_content,
            "video_context": context,
        }
    )

    result = operation.result(timeout=600)
    return result.annotation_results[0].face_detection_annotations





def extract_faces_and_generate_json(face_annotations, input_path, video_id):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise Exception("Error opening video file")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    enriched_data = {
        "video_id": video_id,
        "faces": []
    }

    for annotation in face_annotations:
        for track in annotation.tracks:

            objects = track.timestamped_objects

            if not objects:
                continue

            # Pick middle frame of track (stable representative frame)
            best_object = objects[len(objects) // 2]

            time_offset = (
                    best_object.time_offset.seconds
                    + best_object.time_offset.microseconds / 1e6
            )

            # Jump to exact timestamp
            cap.set(cv2.CAP_PROP_POS_MSEC, time_offset * 1000)
            success, frame = cap.read()

            if not success:
                continue

            box = best_object.normalized_bounding_box

            # Convert normalized box → pixel coordinates safely
            x1 = max(0, int(box.left * width))
            y1 = max(0, int(box.top * height))
            x2 = min(width, int(box.right * width))
            y2 = min(height, int(box.bottom * height))

            # Prevent invalid crop
            if x2 <= x1 or y2 <= y1:
                continue

            face_crop = frame[y1:y2, x1:x2]

            if face_crop.size == 0:
                continue

            # Unique filename using UUID
            unique_name = f"{video_id}_{uuid.uuid4().hex}.jpg"

            cv2.imwrite(unique_name, face_crop)

            try:
                upload_result = cloudinary.uploader.upload(
                    unique_name,
                    folder=f"metavid_faces/{video_id}",
                    resource_type="image"
                )

                image_url = upload_result.get("secure_url")

            except Exception as e:
                print("Cloudinary upload failed:", e)
                os.remove(unique_name)
                continue

            os.remove(unique_name)

            # Extract attributes safely
            attributes = {}
            for attr in best_object.attributes:
                attributes[attr.name] = round(attr.confidence, 4)

            enriched_data["faces"].append({
                "timestamp": round(time_offset, 2),
                "image_url": image_url,
                "attributes": attributes
            })

    cap.release()
    return enriched_data


def annotate_video(face_annotations,input_path,silent_path):
    print("Bounding boxes started....")
    cap = cv2.VideoCapture(input_path)


    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        silent_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_index / fps

        for annotation in face_annotations:
            for track in annotation.tracks:
                start = (
                    track.segment.start_time_offset.seconds
                    + track.segment.start_time_offset.microseconds / 1e6
                )
                end = (
                    track.segment.end_time_offset.seconds
                    + track.segment.end_time_offset.microseconds / 1e6
                )

                if start <= current_time <= end:
                    closest = min(
                        track.timestamped_objects,
                        key=lambda obj: abs(
                            (
                                obj.time_offset.seconds
                                + obj.time_offset.microseconds / 1e6
                            ) - current_time
                        ),
                    )

                    box = closest.normalized_bounding_box

                    x1 = int(box.left * width)
                    y1 = int(box.top * height)
                    x2 = int(box.right * width)
                    y2 = int(box.bottom * height)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2,
                    )

        out.write(frame)
        frame_index += 1

    cap.release()
    out.release()
    print("Bounding boxes ended....")


def merge_audio_with_ffmpeg(input_path, silent_path, result_path):
    print("Merging Audio started....")

    cmd = [
        FFMPEG_PATH,
        "-y",
        "-i", silent_path,
        "-i", input_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        result_path,
    ]

    subprocess.run(cmd, check=True)
    print("DONE ✅ Video + Audio restored 🎧")




# input_path=f"testing/face_results"
# face_annotations = detect_faces(input_path)
#
# json_data = extract_faces_and_generate_json(face_annotations, input_path)
#
#
#
#
# with open("face_results.json", "w") as f:
#     json.dump(json_data, f, indent=4)
