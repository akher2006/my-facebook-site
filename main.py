@app.route("/post/new", methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        post_content = request.form.get('content')
        new_post = Post(content=post_content, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')