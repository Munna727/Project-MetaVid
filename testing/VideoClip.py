from moviepy import VideoFileClip, concatenate_videoclips

clip=VideoFileClip("Assets/newyork.mp4")
clip2=VideoFileClip("Assets/processed_uploads/shots_change.mp4")
newsubclip=clip.subclipped(2,5)
newsubclip2=clip2.subclipped(5,8)
newsubclip.write_videofile("Assets/clipped1.mp4")
newsubclip2.write_videofile("Assets/clipped2.mp4")
clips=[]
clips.append(newsubclip)
clips.append(newsubclip2)
finalclip=concatenate_videoclips(clips,method="compose")
finalclip.write_videofile("Assets/finalclip.mp4")