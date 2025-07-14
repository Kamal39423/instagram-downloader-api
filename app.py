from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Instagram Downloader API is Running'})

@app.route('/api', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        options = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            media_url = info.get('url')
            is_video = media_url.endswith('.mp4') or info.get('ext') == 'mp4'

            return jsonify({
                'title': info.get('title'),
                'type': 'video' if is_video else 'image',
                'media': media_url
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
