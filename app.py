from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
from functools import wraps

app = Flask(__name__)

TOKEN = os.getenv('TOKEN') or str(uuid.uuid4())
app.logger.warning(f"Token: {TOKEN}")

def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        provided_token = request.args.get('token')

        if not provided_token:
            return jsonify({"error": "token is required."}), 401

        if provided_token != TOKEN:
            return jsonify({"error": "invalid token."}), 401

        return func(*args, **kwargs)

    return wrapper

@app.route('/download', methods=['GET'])
@check_token
def download_video():
    video_url = request.args.get('url')
    output_template = request.args.get('output_template', '%(id)s.%(ext)s')

    if not video_url:
        return jsonify({"error": "please provide a video url."}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            file_name = ydl.prepare_filename(info)
            ydl.download([video_url])
        except yt_dlp.DownloadError as e:
            return jsonify({"error": f"error downloading the video: {str(e)}"}), 500

    try:
        response = send_file(file_name, as_attachment=True)
        os.remove(file_name)
        return response
    except Exception as e:
        return jsonify({"error": f"error sending the file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
