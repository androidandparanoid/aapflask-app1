from flask import Flask,render_template,request,redirect,flash,abort,session,jsonify #request required to handle forms
from flask.helpers import url_for
import json
import os.path

app = Flask(__name__)
app.secret_key = "Welcome1"

@app.route('/')
def index():
    return render_template('index.html',codes=session.keys())#to passon the session add codes, then edit index.html

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/your-url', methods=[ 'GET','POST'])#you need to explicitely define methods
def yoururl():
    if request.method == 'POST':
        #return render_template('yoururl.html', code=request.args['code'],url=request.args['url']) this can be used for GET Methods
        urls = {}#empty dict to store form information

        #This block will validate if json file exists and will append url to it
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)
        #if the shorthand already exists, it will redirect the user back to index
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please use another name')#flash is a function that allows to send messages, flash requires a secret key for it to work. Secret at line #7
            return redirect(url_for('index'))
        else:
            urls[request.form['code']] = {'url': request.form['url']}
            with open('urls.json','w') as url_file:
                json.dump(urls, url_file)
                session[request.form['code']]=True #This will activate the session for the user, you can also use a timestamp, if you had any previous json files, you need to delete it in order to activate the session.
        
        return render_template('yoururl.html', code=request.form['code'],url=request.form['url'])
    else:
        #return '<h1>This is not a valid request</h1>'
        return redirect(url_for('index'))#first param is the function to return

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():                        
                    return redirect(urls[code]['url'])
    return abort(404)

#Create a custom error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pagenotfound.html'),404 #when 4040 occurs it will return the template

@app.route('/api')
def session_api():
    #we want to retrieve session data and pass it on jsonify
    return jsonify(list(session.keys()))

        
                


if __name__ == "__main__":       
    app.run()