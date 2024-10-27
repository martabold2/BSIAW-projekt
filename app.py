from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {'user1': 'password1', 'user2': 'password2'}
comments = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('forum.html', name=name, comments=comments)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user_id'] = username
            return redirect(url_for('success', name=username))
        else:
            return "Invalid credentials, please try again."
    else:
        return render_template('login.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    content = request.form['content']
    username = session['user_id']

    comments.append({'username': username, 'content': content})

    return redirect(url_for('success', name=username))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
