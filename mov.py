#Create video
from moviepy.editor import ColorClip, concatenate_videoclips, AudioFileClip
import gc
from  main import getPeakTimes
import numpy as np

gc.collect()
peak_times_r = getPeakTimes()
gc.collect()

# width = 400
# height = 400
# colors = [
#     [255, 0, 0],
#     [0, 255, 0],
#     [0, 0, 255],
#     [0, 0, 0],
#     [255, 255, 255]          
# ]
# curColor = 0
# allClips = []
# for i in range(len(peak_times_r)):
#     dur = 0
#     if i == 0:
#         dur = peak_times_r[0]
#     else:
#         dur = peak_times_r[i] - peak_times_r[i-1]
#     clip = ColorClip((width, height), color=np.array(colors[curColor], dtype=np.uint8), duration=dur)
#     allClips.append(clip)
#     curColor = (curColor + 1) % len(colors)
# print("Starting Frame Composition")
# audClip = AudioFileClip("./exp.wav")
# finalClip = concatenate_videoclips(allClips)
# finalClip = finalClip.set_audio(audClip)
# finalClip.fps = 10

# finalClip.write_videofile('test.mp4')

# audClip.close()
# finalClip.close()
# for clip in allClips:
#     clip.close()

# Parameters
width, height = 400, 400
colors = [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [0, 0, 0],
    [255, 255, 255]
]
curColor = 0

batch_size = 500  # Adjust batch size based on system memory
batched_clips = []
start_idx = 0

# Process in batches
print("Starting Frame Composition")
for batch_start in range(0, len(peak_times_r), batch_size):
    allClips = []
    batch_end = min(batch_start + batch_size, len(peak_times_r))
    for i in range(batch_start, batch_end):
        dur = peak_times_r[i] - peak_times_r[i-1] if i > 0 else peak_times_r[0]
        clip = ColorClip((width, height), color=np.array(colors[curColor], dtype=np.uint8), duration=dur)
        allClips.append(clip)
        curColor = (curColor + 1) % len(colors)

    # Concatenate batch
    batched_clip = concatenate_videoclips(allClips)
    batched_clips.append(batched_clip)

    # Clean up memory for individual clips
    for clip in allClips:
        clip.close()

# Combine all batched clips
finalClip = concatenate_videoclips(batched_clips)

# Add audio
audClip = AudioFileClip("./exp.wav")
finalClip = finalClip.set_audio(audClip)
finalClip.fps = 10

# Save output
print("Writing Video File")
finalClip.write_videofile('test.mp4')

# Cleanup
audClip.close()
finalClip.close()
for batch in batched_clips:
    batch.close()