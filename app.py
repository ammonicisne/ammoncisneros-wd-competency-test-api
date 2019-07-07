from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
CORS(app)

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    category = db.Column(db.String(15), nullable=False, unique=False)
    content = db.Column(db.String(200))

    def __init__(self, title, category, content):
        self.title = title
        self.category = category
        self.content = content

@app.route("/article/input", methods=["POST"])
def article_input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get("title")
        category = post_data.get("category")
        content = post_data.get("content")
        record = Article(title, category, content)
        db.session.add(record)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Something went wrong, I'm sorry")

@app.route("/articles", methods=["GET"])
def get_articles():
    all_articless = db.session.query(Article.id, Article.title, Article.category, Article.content).all()
    return jsonify(all_articles)

@app.route("/article/<id>", methods=["GET"])
def get_article_by_id(id):
    one_article = db.session.query(Article.id, Article.title, Article.category, Article.content).filter(Article.id == id).first()
    return jsonify(one_article)

@app.route("/article/update/<id>", methods=["PUT"])
def update_article(id):
    if request.content_type == "application/json":
        put_data = request.get_json()
        new_title = put_data.get("title")
        new_category = put_data.get("category")
        new_content = put_data.get("content")
        record = db.session.query(Article).get(id)
        record.title = new_title
        record.category = new_category
        record.content = new_content
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Something went wrong...")

@app.route("/article/delete", methods=["DELETE"])
def delete_article():
    if request.content_type == "application/json":
        delete_data = request.get_json()
        article_id = delete_data.get("id")
        record = db.session.query(Article).get(article_id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Deleted Article")
    return jsonify("Something went wrong")
    

if __name__ == "__main__":
    app.debug = True
    app.run()