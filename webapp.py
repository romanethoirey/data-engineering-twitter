
from flask import Flask, request, render_template

app = Flask(__name__)

def get_N_Most_Similar_Tweets(sentence, n=20):
    tweets = []
    for i in range(1,int(n)+1):
        tweets.append("Top "+str(i)+" similar tweet")
    return tweets

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        details = request.form
        if (details['form_type'] == 'analysis_sentence'):
            content = details['sentence']
            tweets = get_N_Most_Similar_Tweets(details['sentence'], details['topN'])
            return render_template('index.html', content=content, tweets=tweets)
    return render_template('index.html', content='', tweets=-1)

if __name__ == '__main__':
    app.run(host='0.0.0.0')