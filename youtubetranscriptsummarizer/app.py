from flask import Flask, render_template,request, make_response, jsonify, abort
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)


def get_trans(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=(['en']))
    data=''
    for i in transcript:
        data+=i['text']
        data+=' '
    return(data)


def summarize(id_video):
    data = get_trans(id_video)
    summarizer = pipeline('summarization')
    num_iter = int(len(data)/1000)
    summarized_text = []
    for i in range(0, num_iter + 1):
        start = 0
        start = i*1000
        end = (i+1)*1000
        out = summarizer(data[start:end], min_length = 10, max_length = 50)
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
    summary = ' '.join(summarized_text)
    return(summary)


def retrieve_summary(url):
    video_id = url.split("=")[1]
    return(summarize(video_id))


@app.route('/')
def hello():
    return(render_template("index.html"))


@app.route('/api/summarize', methods=['GET'])
def index(): 
    url = request.args.get('youtube_url', '')
    transcript = retrieve_summary(url)
    if len(transcript)==0:
        abort(404)
    return transcript


@app.errorhandler(404)
def not_found(self):
    return make_response(jsonify({'error':'Not found'}),404)


if __name__== '__main__':
    app.run(debug=True)





