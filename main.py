from flask import Flask, render_template, request
import uuid
import os
from plugins import face_output as ft, Cloudinary_test as ct
from plugins import logo_recognition as lr
from plugins import object_track as ot
from plugins import Shot_test as st

app = Flask(__name__)

BUCKET_NAME="metavid-bucket"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/team")
def team():
    return render_template("team.html")

# @app.route("/features")
# def features():
#     return render_template("team.html")


@app.route("/shots", methods=["GET", "POST"])
def shot_feature():
    return render_template("shot.html")


@app.route('/face',methods=["GET","POST"])
def face_feature():
    return render_template("Face.html")



@app.route('/logos',methods=["GET","POST"])
def logos_feature():
    return render_template("Logos.html")

@app.route("/objects",methods=["GET","POST"])
def object_feature():
    return render_template("ObjectTrack.html")


@app.route("/shotchangedetection", methods=["GET", "POST"])
def shotDetection()-> None:
    video= request.files["video"]
    job_id = str(uuid.uuid4())
    input_path = f"Assets/user_uploads/{job_id}_upload.mp4"
    video.save(input_path)
    shots= st.analyze_shots(input_path)
    url=ct.cloudinary_upload(input_path)
    os.remove(input_path)
    return render_template("shot.html",shots=shots,url=url)



@app.route("/facedetection", methods=["POST"])
def face_detection():
    video = request.files["video"]

    job_id = str(uuid.uuid4())

    input_path = f"Assets/user_uploads/{job_id}_upload.mp4"
    silent_path = f"Assets/processed_uploads/{job_id}_silent.mp4"
    result_path = f"Assets/processed_uploads/{job_id}_result.mp4"

    video.save(input_path)


    # 1️⃣ Detect faces + attributes
    face_annotations = ft.detect_faces(input_path)

    # 2️⃣ Extract cropped faces + upload to Cloudinary + build JSON
    face_json = ft.extract_faces_and_generate_json(
        face_annotations,
        input_path,
        job_id
    )

    # 3️⃣ Annotate video
    ft.annotate_video(face_annotations, input_path, silent_path)

    # 4️⃣ Restore audio
    ft.merge_audio_with_ffmpeg(input_path, silent_path, result_path)

    # 5️⃣ Upload final annotated video
    video_url = ct.cloudinary_upload(result_path)

    # Cleanup local files
    os.remove(input_path)
    os.remove(silent_path)
    os.remove(result_path)

    return render_template(
        "Face.html",
        url=video_url,
        face_data=face_json["faces"]
    )





@app.route("/logosrecognition", methods=["POST"])
def logo_recognition():

    video = request.files["video"]
    job_id = str(uuid.uuid4())

    input_path = f"Assets/user_uploads/{job_id}_upload.mp4"
    silent_path = f"Assets/processed_uploads/{job_id}_silent.mp4"
    result_path = f"Assets/processed_uploads/{job_id}_result.mp4"

    video.save(input_path)

    # Detect logos
    annotation_result = lr.detect_logo(input_path)

    # Annotate + get logo JSON
    detected_logos = lr.annotate_video_with_logos(
        input_path,
        silent_path,
        annotation_result
    )

    # Merge audio
    ft.merge_audio_with_ffmpeg(input_path, silent_path, result_path)

    # Upload final processed video
    url = ct.cloudinary_upload(result_path)

    # Cleanup
    if url:
        os.remove(input_path)
        os.remove(silent_path)
        os.remove(result_path)

    return render_template(
        "Logos.html",
        url=url,
        detected_logos=detected_logos
    )



@app.route("/Objecttracking", methods=["POST"])
def object_tracking():

    video = request.files["video"]
    job_id = str(uuid.uuid4())

    input_path = f"Assets/user_uploads/{job_id}_upload.mp4"
    silent_path = f"Assets/processed_uploads/{job_id}_silent.mp4"
    result_path = f"Assets/processed_uploads/{job_id}_result.mp4"

    video.save(input_path)

    # 1️⃣ Detect
    object_annotations = ot.object_tracker(input_path)

    # 2️⃣ Extract JSON + Upload Crops
    object_json = ot.extract_objects_and_generate_json(
        object_annotations,
        input_path,
        job_id
    )

    # 3️⃣ Annotate Video
    ot.annotate_video_with_object_tracking(
        input_path,
        silent_path,
        object_annotations
    )

    # 4️⃣ Restore Audio
    ft.merge_audio_with_ffmpeg(input_path, silent_path, result_path)

    # 5️⃣ Upload Final Video
    video_url = ct.cloudinary_upload(result_path)

    os.remove(input_path)
    os.remove(silent_path)
    os.remove(result_path)

    return render_template(
        "ObjectTrack.html",
        url=video_url,
        object_data=object_json["objects"]
    )


if __name__ == '__main__':
    app.run(debug=True)
