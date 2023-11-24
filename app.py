from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    output_template = request.args.get('output_template', '%(id)s.%(ext)s')

    if not video_url:
        return jsonify({"error": "please provide a video URL."}), 400

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
