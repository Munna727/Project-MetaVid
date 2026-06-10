import io
import  os
import uuid
import cloudinary
import cloudinary.uploader
import cv2
from google.cloud import videointelligence


def detect_logo(local_file_path):

    client = videointelligence.VideoIntelligenceServiceClient()

    with io.open(local_file_path, "rb") as f:
        input_content = f.read()

    features = [videointelligence.Feature.LOGO_RECOGNITION]

    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )

    print("Waiting for operation to complete...")
    response = operation.result()

    annotation_result = response.annotation_results[0]

    return annotation_result


# ---------- Modern Rounded Rectangle ----------
def draw_rounded_rect(img, pt1, pt2, color, thickness=2, radius=8):
    x1, y1 = pt1
    x2, y2 = pt2

    # Horizontal lines
    cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)

    # Vertical lines
    cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

    # Corner arcs
    cv2.ellipse(img, (x1 + radius, y1 + radius),
                (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y1 + radius),
                (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x1 + radius, y2 - radius),
                (radius, radius), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y2 - radius),
                (radius, radius), 0, 0, 90, color, thickness)


def annotate_video_with_logos(input_video_path, output_video_path, annotation_result):

    cap = cv2.VideoCapture(input_video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    BOX_COLOR = (235, 99, 37)
    TEXT_COLOR = (255, 255, 255)
    FONT = cv2.FONT_HERSHEY_SIMPLEX

    frame_annotations = {}
    uploaded_logos = {}
    logo_json_output = []

    # -------- Build Frame Map --------
    for logo in annotation_result.logo_recognition_annotations:
        entity_name = logo.entity.description

        for track in logo.tracks:
            if track.confidence < 0.6:
                continue

            for obj in track.timestamped_objects:
                time_sec = (
                    obj.time_offset.seconds
                    + obj.time_offset.microseconds / 1e6
                )

                frame_no = int(time_sec * fps)
                box = obj.normalized_bounding_box

                frame_annotations.setdefault(frame_no, []).append(
                    (entity_name, box)
                )

    frame_idx = 0
    local_files=[]
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx in frame_annotations:
            for entity_name, box in frame_annotations[frame_idx]:

                x1 = int(box.left * width)
                y1 = int(box.top * height)
                x2 = int(box.right * width)
                y2 = int(box.bottom * height)

                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)

                label = entity_name.lower()
                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    FONT,
                    0.6,
                    TEXT_COLOR,
                    1,
                    cv2.LINE_AA
                )

                # --------- Upload Logo Crop (Only Once Per Logo) ---------
                if entity_name not in uploaded_logos:

                    cropped_logo = frame[y1:y2, x1:x2]

                    if cropped_logo.size != 0:
                        temp_filename = f"{uuid.uuid4()}.jpg"
                        cv2.imwrite(temp_filename, cropped_logo)
                        local_files.append(temp_filename)
                        upload_result = cloudinary.uploader.upload(
                            temp_filename,
                            folder="detected_logos"
                        )

                        logo_url = upload_result["secure_url"]

                        uploaded_logos[entity_name] = logo_url

                        logo_json_output.append({
                            "logo_name": entity_name,
                            "logo_image_url": logo_url
                        })

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()

    print("Bounding boxes completed")
    for file in local_files:
        if os.path.exists(file):
            os.remove(file)
    return logo_json_output
