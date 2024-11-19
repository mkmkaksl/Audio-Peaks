from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np

file = "./audio/test.wav"

rate, data = wavfile.read(file)
print(rate)
length = data.shape[0]

if data.ndim > 1:
    right_data = data[:, 0]
    left_data = data[:, 1]

buffer = 5000
prominence = 500

peaks_r, peaks_props = find_peaks(right_data, prominence = prominence)
mins_r, mins_props = find_peaks(-right_data, prominence = prominence)

peak_times_r = peaks_r / rate
min_times_r = mins_r / rate

print(peak_times_r)
print(len(peak_times_r))

new_signal_right = np.zeros_like(right_data)
for peak in peaks_r:
    new_signal_right[peak-buffer:peak+buffer] = right_data[peak-buffer:peak+buffer]

for minA in mins_r:
    new_signal_right[minA-buffer:minA+buffer] = right_data[minA-buffer:minA+buffer]

peaks_l, peaks_props = find_peaks(left_data, prominence = prominence)
mins_l, mins_props = find_peaks(-left_data, prominence = prominence)

peak_times_l = peaks_l / rate
min_times_l = mins_l / rate

new_signal_left = np.zeros_like(left_data)
for peak in peaks_l:
    new_signal_left[peak-buffer:peak+buffer] = left_data[peak-buffer:peak+buffer]

for minA in mins_l:
    new_signal_left[minA-buffer:minA+buffer] = left_data[minA-buffer:minA+buffer]
# new_signal_left[peaks-buffer:peaks+buffer] = left_data[peaks-buffer:peaks+buffer]
# new_signal_left[mins-buffer:mins+buffer] = left_data[mins-buffer:mins+buffer]
print("Created left signal")

new_signal = np.column_stack([new_signal_right, new_signal_left])
wavfile.write("exp.wav", rate, new_signal.astype(data.dtype))
print("Created new file")

#Create video
from moviepy.editor import *
width = 920
height = 920
colors = "red blue yellow white black".split(" ")
curColor = 0
allClips = []
for i in range(len(peak_times_r)):
    dur = 0
    if i == 0:
        dur = peak_times_r[0]
    else:
        dur = peak_times_r[i] - peak_times_r[i-1]
    clip = ColorClip((width, height), color=colors[curColor], duration=dur)
    allClips.append(clip)

audClip = AudioFileClip("./exp.wav")
finalClip = concatenate_videoclips(allClips)
finalClip.set_audio(audClip)

finalClip.write_videofile('test.mp4')