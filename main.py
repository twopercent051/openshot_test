import os
import time
from requests import get, post
from requests.auth import HTTPBasicAuth
from test import clip_json

PATH = os.path.dirname(os.path.realpath(__file__))
CLOUD_URL = 'http://cloud.openshot.org'
CLOUD_AUTH = HTTPBasicAuth('demo-cloud', 'demo-password')


##########################################################
# Get list of projects
end_point = '/projects/'
r = get(CLOUD_URL + end_point, auth=CLOUD_AUTH)
print(r.json())


##########################################################
# Create new project
end_point = '/projects/'
project_data = {
    "name": "API Project",
    "width": 1920,
    "height": 1080,
    "fps_num": 30,
    "fps_den": 1,
    "sample_rate": 44100,
    "channels": 2,
    "channel_layout": 3,
    "json": "{}",
}
r = post(CLOUD_URL + end_point, data=project_data, auth=CLOUD_AUTH)
print(r.json())
project_id = r.json().get("id")
project_url = r.json().get("url")


##########################################################
# Upload file to project
end_point = '/projects/%s/files/' % project_id
source_path = os.path.join(PATH, "video_2022-12-18_14-07-57.mp4")
source_name = os.path.split(source_path)[1]
file_data = {
    "media": None,
    "project": project_url,
    "json": "{}"
}
r = post(CLOUD_URL + end_point, data=file_data, files={"media": (source_name, open(source_path, "rb"))}, auth=CLOUD_AUTH)
file_url = r.json().get("url")
print(r.json())


##########################################################
# Create a clip for the previously uploaded file
end_point = '/projects/%s/clips/' % project_id
clip_data = {
    "file": file_url,
    "position": 0.0,
    "start": 0.0,
    "end": 20.0,
    "layer": 1,
    "project": project_url,
    "json": clip_json
    # "json": '{}'
}
r = post(CLOUD_URL + end_point, data=clip_data, auth=CLOUD_AUTH)
print('CLIP: ' + str(r.json()))


##########################################################
# Create effects
# end_point = '/projects/%s/effects/' % project_id
#
# effects_data = {
#     "title": "Pixelate",
#     "type": "Wave",
#     "position": 0.0,
#
#     "start": 0.0,
#     "end": 10.0,
#     "layer": 1,
#     "project": project_url,
#     'Amplitude': 0.7,
#     'json': '{}'
# }
# r = post(CLOUD_URL + end_point, data=effects_data, auth=CLOUD_AUTH)
# # effects_url = r.json().get("url")
# print(r.json())


##########################################################
# Create export for final rendered video
end_point = '/projects/%s/exports/' % project_id
export_data = {
    "video_format": "mp4",
    "video_codec": "libx264",
    "video_bitrate": 8000000,
    "audio_codec": "ac3",
    "audio_bitrate": 1920000,
    "start_frame": 1,
    "end_frame": 10,
    "project": project_url,
    "json": "{}"
}
r = post(CLOUD_URL + end_point, data=export_data, auth=CLOUD_AUTH)
export_url = r.json().get("url")
print(r.json())


##########################################################
# Wait for Export to finish (give up after around 40 minutes)
export_output_url = None
is_exported = False
countdown = 500
while not is_exported and countdown > 1:
    r = get(export_url, auth=CLOUD_AUTH)
    print(r.json().get("progress", 0.0))
    is_exported = float(r.json().get("progress", 0.0)) == 100.0
    countdown -= 1
    time.sleep(1.0)

# Get final rendered url
r = get(export_url, auth=CLOUD_AUTH)
export_output_url = r.json().get("output")
print(r.json())
print("Export Successfully Completed: %s!" % export_output_url)