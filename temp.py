# from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
# import requests
# from moviepy.config import change_settings
# from PIL import Image
# from win32com.client import Dispatch
# import time
# import os
#
# # from win32com.client import Dispatch
# #
# # # Function to list all available SAPI voices
# # def list_available_voices():
# #     try:
# #         speech = Dispatch("SAPI.SpVoice")
# #         voices = speech.GetVoices()
# #         for i in range(voices.Count):
# #             voice = voices.Item(i)
# #             print(f"Voice {i}: {voice.GetDescription()}")
# #     except Exception as e:
# #         print(f"Error occurred: {str(e)}")
# #
# # # Call the function to list all voices
# # list_available_voices()
#
#
#
#
# change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
# # "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
#
#
# API_KEY = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
# BASE_URL = 'https://api.pexels.com/videos/search'
# HEADERS = {
#     'Authorization': API_KEY,
#     'Accept': 'application/json',
# }
#
#
# def check_rate_limits():
#     url = f"{BASE_URL}?query=example&per_page=1"  # Example query to fetch minimal data
#     response = requests.get(url, headers=HEADERS)
#
#     if response.status_code == 200:
#         limit = response.headers.get('X-Ratelimit-Limit')
#         remaining = response.headers.get('X-Ratelimit-Remaining')
#         reset_timestamp = int(response.headers.get('X-Ratelimit-Reset'))
#
#         reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_timestamp))
#
#         print(f"Total monthly limit: {limit}")
#         print(f"Remaining requests: {remaining}")
#         print(f"Reset time: {reset_time}")
#     else:
#         print(f"Error fetching rate limits: {response.status_code} - {response.text}")
#
#
#
# def speak(text, output_file):
#     try:
#         speech = Dispatch("SAPI.SpVoice")
#         voices = speech.GetVoices()
#
#         specific_voice_index = 0
#         if specific_voice_index < len(voices):
#             speech.Voice = voices.Item(specific_voice_index)
#         else:
#             print(f"Voice index {specific_voice_index} is out of range. Using default voice.")
#
#         file_stream = Dispatch("SAPI.SpFileStream")
#         file_stream.Open(output_file, 3)  # 3 means open for writing
#         speech.AudioOutputStream = file_stream
#         speech.Speak(text)
#         file_stream.Close()
#         print(f"Audio file saved to {output_file}")
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#
#
# # def text_to_speech(script, output_file):
# #     tts = gTTS(text=script, lang='en')
# #     tts.save(output_file)
# #     print(f"Audio content written to file {output_file}")
#
# # def fetch_video_clips(topic, num_videos=10):
# #     api_key = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
# #     url = f"https://api.pexels.com/videos/search?query={topic}&per_page=5"
# #     headers = {"Authorization": api_key}
# #     response = requests.get(url, headers=headers)
# #     videos = response.json()['videos']
# #     return [video['video_files'][0]['link'] for video in videos]
#
#
# # def fetch_video_clips(topics, orientation, max_duration=20, num_videos=16, retries=3):
# #     api_key = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
# #     topics_query = '|'.join(topics)
# #     url = f"https://api.pexels.com/videos/search?query={topics_query}&orientation={orientation}&max_duration={max_duration}&per_page=80"
# #     headers = {"Authorization": api_key}
# #     all_videos = []
# #     page = 1
# #
# #     while len(all_videos) < num_videos:
# #         try:
# #             response = requests.get(url + f"&page={page}", headers=headers)
# #             response.raise_for_status()  # Check if the request was successful
# #             videos = response.json().get('videos', [])
# #             if not videos:
# #                 break
# #
# #             # Filter videos by resolution and length if necessary
# #             for video in videos:
# #                 video_url = video['video_files'][0]['link']
# #                 video_duration = video['duration']
# #                 video_resolution = video['video_files'][0]['quality']
# #
# #                 if video_resolution == 'hd' and video_duration > 10:  # Adjust conditions as needed
# #                     all_videos.append(video_url)
# #                     if len(all_videos) >= num_videos:
# #                         break
# #             page += 1
# #
# #         except requests.exceptions.RequestException as e:
# #             print(f"An error occurred: {e}")
# #             retries -= 1
# #             if retries == 0:
# #                 print("Max retries exceeded. Exiting...")
# #                 break
# #             print("Retrying...")
# #             time.sleep(5)  # Wait before retrying
# #
# #     return all_videos
#
# def fetch_video_clips_from_folder(folder_path, num_videos=16):
#     all_videos = []
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
#                 all_videos.append(os.path.join(root, file))
#                 if len(all_videos) >= num_videos:
#                     break
#         if len(all_videos) >= num_videos:
#             break
#     return all_videos
#
#
# def create_video(video_urls, audio_file, output_file):
#     video_clips = [VideoFileClip(url) for url in video_urls]
#     final_clip = concatenate_videoclips(video_clips)
#
#     audio = AudioFileClip(audio_file)
#     final_clip = final_clip.set_audio(audio)
#
#     video_with_captions = CompositeVideoClip([final_clip])
#     video_with_captions.write_videofile(output_file, codec="libx264", audio_codec="aac")
#
#
# # def create_video(video_urls, audio_file, output_file):
# #     # Load all video clips and resize to a common resolution
# #     video_clips = []
# #     for url in video_urls:
# #         clip = VideoFileClip(url)
# #         print(clip)
# #         clip_resized = clip.resize(width=1920,height=1080)  # For landscape video
# #         # clip_resized = clip.resize(height=1920)  # For portrait video
# #         video_clips.append(clip_resized)
# #
# #     # Concatenate video clips
# #     final_clip = concatenate_videoclips(video_clips)
# #
# #     # Set audio from the generated speech
# #     audio = AudioFileClip(audio_file)
# #     final_clip = final_clip.set_audio(audio)
# #
# #     # Write final video file
# #     final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate="5000k", fps=30, preset="slow")
#
# def count_video_clips(folder_path):
#     video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']  # Add more extensions as needed
#     video_clip_count = 0
#
#     entries = os.listdir(folder_path)
#     for entry in entries:
#         if any(entry.endswith(ext) for ext in video_extensions):
#             video_clip_count += 1
#
#     return video_clip_count
#
# def main(folder_path, num_videos):
#     with open("script.txt") as f:
#         script = f'''{f.read()}'''
#
#     audio_file = "spoken_audio.wav"
#     speak(script, audio_file)
#     # video_urls = fetch_video_clips(topics, orientation, duration, videos)
#     video_files = fetch_video_clips_from_folder(folder_path, num_videos)
#     create_video(video_files, audio_file, "output_video.mp4")
#
#
# if __name__ == "__main__":
#     folder_path = "C://Users//aryan//PycharmProjects//pythonProject//video_clips"
#     num_videos = count_video_clips(folder_path)
#     main(folder_path, num_videos)



from gtts import gTTS
import os

text = "नमस्ते, यह एक उदाहरण है"
tts = gTTS(text=text, lang='hi')
tts.save("output.mp3")
os.system("start output.mp3")  # Play the audio


