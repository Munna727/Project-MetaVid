"""Transcribe speech from a video stored on GCS."""
from google.cloud import videointelligence

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]

config = videointelligence.SpeechTranscriptionConfig(
    language_code="te-IN", enable_automatic_punctuation=True
)
video_context = videointelligence.VideoContext(speech_transcription_config=config)
with open(r"Assets/speech.mp4", "rb") as f:
    video_content = f.read()

operation = video_client.annotate_video(
    request={
        "features": features,
        "input_content": video_content,
        "video_context": video_context,
    }
)

print("\nProcessing video for speech transcription.")

result = operation.result(timeout=600)

# There is only one annotation_result since only
# one video is processed.
annotation_results = result.annotation_results[0]

for speech_transcription in annotation_results.speech_transcriptions:

    for i, alt in enumerate(speech_transcription.alternatives):
        print(i, alt.transcript, alt.confidence)

        # print("Word level information:")
        # for word_info in alternative.words:
        #     word = word_info.word
        #     start_time = word_info.start_time
        #     end_time = word_info.end_time
        #     print(
        #         "\t{}s - {}s: {}".format(
        #             start_time.seconds + start_time.microseconds * 1e-6,
        #             end_time.seconds + end_time.microseconds * 1e-6,
        #             word,
        #         )
        #     )


    # The number of alternatives for each transcription is limited by
    # SpeechTranscriptionConfig.max_alternatives.
    # Each alternative is a different possible transcription
    # and has its own confidence score.
    # for alternative in speech_transcription.alternatives:
    #     print("Alternative level information:")
    #
    #     print("Transcript: {}".format(alternative.transcript))
    #     print("Confidence: {}\n".format(alternative.confidence))