from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

error_msg = {'title_error':'Please fill in title',
'body_error':'Please fill in the body'}

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.String(300))

    def __init__(self, blog_title, blog_post):
        self.blog_title = blog_title
        self.blog_post = blog_post



@app.route('/blog', methods=['GET', 'POST'])
def blog():
    blog_all = Blog.query.all()
    if request.method == 'POST': 
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        if len(blog_title) <= 0 or len(blog_post) <=0: #Redirects to /new_post if blog title or blog post is empty
            return redirect('/new_post?title_error={title_error}&body_error={body_error}'.format(
                            title_error=error_msg['title_error'], 
                            body_error=error_msg['body_error']))

        new_blog_post = Blog(blog_title, blog_post)
        db.session.add(new_blog_post)
        db.session.commit()
        blog_all = Blog.query.all()
        return render_template('blog.html', blog_all=blog_all, title="Build A Blog")

    
    blog_id = request.args.get('id')
    if blog_id:
        blog_obj = Blog.query.filter_by(id=blog_id).first()
        return render_template('single_blog.html', 
                                single_title=blog_obj.blog_title, 
                                single_post=blog_obj.blog_post) #Renders single blog and passes unique blog title and post to the single_blog template based on the individual object

        
        
    return render_template('blog.html', blog_all=blog_all, title="Build A Blog")

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST': 
        maintain_title = request.form['blog_title']
        maintain_post = request.form['blog_post']
        return render_template('new_post.html', title_error=error_msg['title_error'],
            body_error=error_msg['body_error'])

    title_error = request.args.get('title_error')
    body_error = request.args.get('body_error')
    if title_error == None or body_error == None: #Displays error msg if user input is empty
        title_error = ''
        body_error = ''

    return render_template('new_post.html', title_error=title_error,
        body_error=body_error)

    return render_template('new_post.html')

@app.route('/single_blog', methods=['POST', 'GET'])
def single_blog():
    blog_object = Blog.query.get(int(request.args.get('id'))) # Gets blog object from database using id that was sent as query in url
    single_title = blog_object.blog_title
    single_post = blog_object.blog_post
    return render_template('single_blog.html', single_title=single_title, single_post=single_post)



if __name__ == '__main__':
    app.run()