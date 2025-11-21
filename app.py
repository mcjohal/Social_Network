from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Fake database for new posts (not persisted)
new_posts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    # Jeep-ify some titles for fun
    jeep_keywords = ["Wrangler", "Rubicon", "Overland", "Trail Rated", "Moab", "4x4", "Lift Kit", "37s", "Rock Crawling", "Jeep Wave"]
    for post in posts[:20]:
        post['title'] = f"{post['userId']}x{post['id']} {post['title'].capitalize()} | {jeep_keywords[post['id'] % len(jeep_keywords)]} Build"
    all_posts = posts[:20] + new_posts
    return render_template('posts.html', posts=all_posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}').json()
    comments = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}/comments').json()
    return render_template('post_detail.html', post=post, comments=comments)

@app.route('/users')
def users():
    users = requests.get('https://jsonplaceholder.typicode.com/users').json()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    user = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}').json()
    posts = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}/posts').json()
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_posts.append({
            "id": 999 + len(new_posts),
            "userId": 1,
            "title": title,
            "body": body
        })
        return redirect(url_for('posts'))
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)