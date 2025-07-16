from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

# Define where downloaded files go
downloads_folder = r'C:\ytdlp-web\downloads'
output_template = os.path.join(downloads_folder, '%(title)s.%(ext)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format = request.form['format']

    # Build command based on selected format
    if format == 'mp3':
        cmd = [
            'yt-dlp',
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', output_template,
            url
        ]
    elif format == 'm4a':
        cmd = [
            'yt-dlp',
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'm4a',
            '-o', output_template,
            url
        ]
    elif format == 'mp4':
        cmd = [
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            '-o', output_template,
            url
        ]
    elif format == 'audio':
        cmd = [
            'yt-dlp',
            '-x',
            '-o', output_template,
            url
        ]
    elif format == 'thumbnail':
        cmd = [
            'yt-dlp',
            '--write-thumbnail',
            '--convert-thumbnails', 'png',
            '--skip-download',
            '-o', output_template,
            url
        ]
    else:
        return 'Invalid format selected.', 400

    # Run command and catch output
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f"<h3>Error:</h3><pre>{result.stderr}</pre>", 500
        else:
            return render_template('complete.html')
    except Exception as e:
        return f"<h3>Unexpected error:</h3><pre>{str(e)}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)