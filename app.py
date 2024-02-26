from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import platform

app = Flask(__name__)

def get_downloads_directory():
    # Get the operating system
    operating_system = platform.system()
    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Determine the Downloads directory based on the operating system
    if operating_system == 'Windows':
        downloads_dir = os.path.join(user_home, 'Downloads')
    elif operating_system == 'Linux':
        downloads_dir = os.path.join(user_home, 'Downloads')
    elif operating_system == 'Darwin':  # macOS
        downloads_dir = os.path.join(user_home, 'Downloads')
    else:
        # Default to the user's home directory if the operating system is not recognized
        downloads_dir = user_home
    
    return downloads_dir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Determine the Downloads directory
        downloads_dir = get_downloads_directory()

        # Download the audio stream directly to the Downloads directory
        audio_stream.download(output_path=downloads_dir, filename='audio.mp4')

        # Convert the downloaded audio to MP3 using AudioFileClip
        mp3_file = os.path.join(downloads_dir, 'audio.mp3')
        mp4_file = os.path.join(downloads_dir, 'audio.mp4')

        # Check if the MP4 file exists
        if os.path.exists(mp4_file):
            audio_clip = AudioFileClip(mp4_file)
            audio_clip.write_audiofile(mp3_file)
            audio_clip.close()
            
            # Send the MP3 file as an attachment for download
            return send_file(mp3_file, as_attachment=True)
        else:
            return "Error: MP4 file not found"
    except Exception as e:
        return "Error: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
