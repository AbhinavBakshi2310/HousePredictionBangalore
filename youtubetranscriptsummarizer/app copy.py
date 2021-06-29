from flask import Flask, render_template,request, make_response, jsonify, abort
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
#from transformers import T5ForConditionalGeneration, T5Tokenizer
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

def get_trans(video_id):  #cookie issue
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=(['en']))
    data=''
    for i in transcript:
        data+=i['text']
        data+=' '
        print(len(data))
    return(data)

def summarize(video_id):
    data = get_trans(video_id)
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
    #summary = summarization(data)[0]['summary_text']
    #model = T5ForConditionalGeneration.from_pretrained('t5-base')
    #tokenizer = T5Tokenizer.from_pretrained("t5-base")
    #input = tokenizer.encode("summarize: " + data, return_tensors="pt", max_length= 1024, truncation=True)
    #summary=model.generate(
        #input,
        #max_length=150,
        #min_length=40
        #length_penalty=2.0,
        #num_beams=4,
        #early_stopping=True
    #)
    #return(tokenizer.decode(summary[0]))
    print(len(summary))
    return(summary)


#def get_audio(url):
#    from youtube_dl import YoutubeDL
 #   ydl_opts = {
  #      'format': 'bestaudio/best',
   #     'postprocessors': [{
    #        'key': 'FFmpegExtractAudio',
     #       'preferredcodec': 'mp3'
      #  }],
    #}
    #with YoutubeDL(ydl_opts) as ydl:
       #ydl.download([url])

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        # below is optional for playlists
        if query.path[:9] == '/playlist': return parse_qs(query.query)['list'][0]
       # returns None for invalid YouTube url

def retrieve_summary(url):
    youtube_api=  extract_video_id(url)
    return(summarize(youtube_api))

@app.route('/')
def hello():
    return(render_template("index.html"))

@app.route('/api/summarize', methods=['GET'])
def index(): 
    url = request.args.get('youtube_url', '')
    #url = " "
    transcript = retrieve_summary(url)
    if len(transcript)==0:
        abort(404)
    return transcript



@app.errorhandler(404)
def not_found(self):
    return make_response(jsonify({'error':'Not found'}),404)

if __name__== '__main__':
    app.run(debug=True)





