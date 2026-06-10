import io
from google.cloud import videointelligence
def analyze_shots(video_path):
    """Detects camera shot changes."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
    with io.open(video_path, "rb") as f:
        input_content = f.read()
    operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    print("\nProcessing video for shot change annotations:")

    result = operation.result(timeout=120)
    print("\nFinished processing.")

    shots_list=[]
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (
            shot.start_time_offset.seconds + shot.start_time_offset.microseconds / 1e6
        )
        end_time = (
            shot.end_time_offset.seconds + shot.end_time_offset.microseconds / 1e6
        )
        shots_list.append(
            {"index":i,
             "start":start_time,
             "end":end_time
             })
    return shots_list


