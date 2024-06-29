from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
import requests
from moviepy.config import change_settings
# from PIL import Image
# from gtts import gTTS
from win32com.client import Dispatch
import time
from googletrans import Translator

change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


API_KEY = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
BASE_URL = 'https://api.pexels.com/videos/search'
HEADERS = {
    'Authorization': API_KEY,
    'Accept': 'application/json',
}


def check_rate_limits():
    url = f"{BASE_URL}?query=example&per_page=1"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        limit = response.headers.get('X-Ratelimit-Limit')
        remaining = response.headers.get('X-Ratelimit-Remaining')
        reset_timestamp = int(response.headers.get('X-Ratelimit-Reset'))

        reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_timestamp))

        print(f"Month Limit: {limit}")
        print(f"Remaining requests: {remaining}")
        print(f"Reset time: {reset_time}")
    else:
        print(f"Error: {response.status_code} - {response.text}")



def speak(text, output_file):
    try:
        speech = Dispatch("SAPI.SpVoice")
        voices = speech.GetVoices()

        # 0 - drake voice
        # 1 - hemant hindi voice
        # 2 - kalpana hindi voice
        # 3 - mark voice
        # 4 - zira voice

        specific_voice_index = 3
        if specific_voice_index < len(voices):
            speech.Voice = voices.Item(specific_voice_index)
            # speech.Rate = 2
        else:
            print(f"Voice index {specific_voice_index} is out of range. Using default voice.")

        file_stream = Dispatch("SAPI.SpFileStream")
        file_stream.Open(output_file, 3)
        speech.AudioOutputStream = file_stream
        speech.Speak(text)
        file_stream.Close()
        print(f"Audio file saved to {output_file}")

    except Exception as e:
        print(f"Error : {str(e)}")


def translate_text(text, dest_lang='hi'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

# def text_to_speech(script, output_file):
#     tts = gTTS(text=script, lang='en')
#     tts.save(output_file)
#     print(f"Audio content written to file {output_file}")

# def fetch_video_clips(topic, num_videos=10):
#     api_key = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
#     url = f"https://api.pexels.com/videos/search?query={topic}&per_page=5"
#     headers = {"Authorization": api_key}
#     response = requests.get(url, headers=headers)
#     videos = response.json()['videos']
#     return [video['video_files'][0]['link'] for video in videos]


def fetch_video_clips(topics, orientation, max_duration=20, num_videos=16, retries=3):
    api_key = 'bCddJMS6wnlxNuQcww58OlyqEAVJffM9tdp9dBXPo0thbEozdUXe6X9q'
    topics_query = '|'.join(topics)
    url = f"https://api.pexels.com/videos/search?query={topics_query}&orientation={orientation}&max_duration={max_duration}&per_page=80"
    headers = {"Authorization": api_key}
    all_videos = []
    page = 1

    while len(all_videos) < num_videos:
        try:
            response = requests.get(url + f"&page={page}", headers=headers)
            response.raise_for_status()
            videos = response.json().get('videos', [])
            if not videos:
                break

            for video in videos:
                video_url = video['video_files'][0]['link']
                video_duration = video['duration']
                video_resolution = video['video_files'][0]['quality']

                if video_resolution == 'hd' and video_duration > 10:
                    all_videos.append(video_url)
                    if len(all_videos) >= num_videos:
                        break
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"error: {e}")
            retries -= 1
            if retries == 0:
                print("Max retries over")
                break
            print("Retrying...")
            time.sleep(5)

    return all_videos


# def fetch_video_clips(topics, orientation="horizontal", max_duration=20, num_videos=16, retries=3):
#     api_key = '39307922-a11868d30c1b7338c3b78e679'
#     topics_query = '+'.join(topics)
#     url = f"https://pixabay.com/api/videos/?key={api_key}&q={topics_query}&orientation={orientation}&min_duration=0&mimeType=video/mp4&per_page=200"
#     all_videos = []
#     page = 1
#
#     while len(all_videos) < num_videos:
#         try:
#             response = requests.get(url + f"&page={page}")
#             response.raise_for_status()
#             videos = response.json().get('hits', [])
#             if not videos:
#                 break
#
#             for video in videos:
#                 video_url = video['videos']['large']['url']
#                 all_videos.append(video_url)
#                 if len(all_videos) >= num_videos:
#                     break
#             page += 1
#
#         except requests.exceptions.RequestException as e:
#             print(f"An error occurred: {e}")
#             retries -= 1
#             if retries == 0:
#                 print("Max retries over")
#                 break
#             print("Retrying...")
#             time.sleep(5)
#
#     return all_videos



# def create_video(video_urls, audio_file, output_file):
#     video_clips = [VideoFileClip(url) for url in video_urls]
#     final_clip = concatenate_videoclips(video_clips)
#
#     audio = AudioFileClip(audio_file)
#     final_clip = final_clip.set_audio(audio)
#
#     video_with_captions = CompositeVideoClip([final_clip])
#     video_with_captions.write_videofile(output_file, codec="libx264", audio_codec="aac")


def create_video(video_urls, audio_file, output_file):
    video_clips = []
    for url in video_urls:
        clip = VideoFileClip(url)
        print(clip)
        # clip_resized = clip.resize(width=1920,height=1080)  # landscape video
        clip_resized = clip.resize(height=1920)  # portrait video
        video_clips.append(clip_resized)

    final_clip = concatenate_videoclips(video_clips)

    audio = AudioFileClip(audio_file)
    final_clip = final_clip.set_audio(audio)

    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate="5000k", fps=30, preset="slow")


def main(topics, orientation, duration, videos, lang):
    # with open("script.txt") as f:
    #     script = f'''{f.read()}'''

    file_path = "script.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            script= file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading file: {str(e)}")



    # translated_script = translate_text(script, dest_lang=lang)
    audio_file = "spoken_audio.wav"
    # speak(script, audio_file, lang)
    speak(script, audio_file)
    video_urls = fetch_video_clips(topics, orientation, duration, videos)
    create_video(video_urls, audio_file, "output_video.mp4")


if __name__ == "__main__":
    topics = ["Heat","Temperature","Sun"]
    orientation = "portrait"
    video_max_duration = 10
    num_videos = 4
    lang = 'hi'
    main(topics, orientation, video_max_duration, num_videos, lang)