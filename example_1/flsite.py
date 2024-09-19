from flask import Flask, render_template, flash

app = Flask(__name__)


@app.route("/")
def index():
    # Render a template by name with the given context.
    return render_template('index.html')


@app.route("/about")
@app.route("/about2")
def about():
    return "<h1>О сайте<h1>"


@app.route("/profile/<username>")
def profile(username):
    return f"Пользователь {username}"


@app.route("/profile/<username>/<int:age>")
def age_profile(username, age):
    return f"Пользователь {username}: {age}"


# Test urls with test context
# with app.test_request_context():
#     print('/profile/admin')
#     print('/profile/admin12/12')

if __name__ == '__main__':
    app.run(debug=True)
