from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        # Set the destination directory for the temporary file
        temp_dir = '/temporary-cache'  # Specify your temporary directory
        # Download the audio stream to the temporary directory
        audio_file = video.download(output_path=temp_dir)
        # Rename the downloaded file to have an MP3 extension
        base, _ = os.path.splitext(audio_file)
        mp3_file = base + ".mp3"
        os.rename(audio_file, mp3_file)
        # Send the MP3 file as an attachment for download
        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
