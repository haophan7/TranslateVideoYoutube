import requests
import os
import sys
import time

filename = '/Users/Hao/PycharmProjects/TranslateVideoYoutube/downloads/เรามันต่างกัน we are not same คำอ่านไทย.mp4'
api_key = '301e289ca2aa4894a133e9f0fcbc797b'
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

headers = {
    'authorization': api_key,
    'content-type': 'application/json'
}

response = requests.post(upload_endpoint,
                         headers=headers,
                         data=read_file(filename))

audio_url = response.json()['upload_url']

# STEP 2
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

response = requests.post(transcript_endpoint,
                         headers=headers,
                         json={
                             'audio_url': audio_url,
                         })

transcript_id = response.json()['id']

# STEP 3
polling_endpoint = os.path.join(transcript_endpoint, transcript_id)

status = ''
while status != 'completed':
    response_result = requests.get(
        polling_endpoint,
        headers=headers
    )
    status = response_result.json()['status']
    print(f'Status: {status}')

    if status == 'error':
        sys.exit('Audio file failed to process')
    elif status != 'completed':
        time.sleep(5)

if status == 'completed':
    transcript = response_result.json()['text']
    print(transcript)

    with open('transcript.txt', 'w') as f:
        f.write(transcript)
