from flask import Flask, render_template, redirect, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from config import Config
from datetime import datetime
import sys

app = Flask(__name__)
app.config.from_object(Config)

pages = FlatPages(app)
freezer = Freezer(app)

def get_articles(language):
    # Fetch all articles for the given language
    articles = [page for page in pages if page.meta.get('language') == language]
    # Sort articles by date in descending order (newest first)
    articles.sort(key=lambda page: page.meta.get('date'), reverse=True)
    return articles

@app.route('/')
def index():
    return redirect(url_for('show_posts', language="fi"))

@app.route('/<language>/')
def show_posts(language):
    posts = get_articles(language)
    # Pass datetime to the template context
    return render_template('index.html', posts=posts, language=language, datetime=datetime)

@app.route('/<language>/<path:path>/')
def show_post(language, path):
    post = pages.get_or_404(f'{language}/{path}')
    # Pass datetime to the template context
    return render_template('article.html', post=post, language=language, datetime=datetime)

@freezer.register_generator
def show_posts():
    # Generate static pages for each language
    languages = ['fi', 'en']
    for language in languages:
        yield 'show_posts', {'language': language}

@freezer.register_generator
def show_post():
    # Generate static pages for each language and each article
    languages = ['fi', 'en']
    for language in languages:
        for page in pages:
            if page.meta.get('language') == language:
                # Ensure paths do not include duplicated language segments
                path = page.path
                if path.startswith(f'{language}/'):
                    path = path[len(language) + 1:]  # Remove leading language segment
                # Debug print statement to see the URLs being generated
                print(f'Generating URL for show_post with language={language} and path={path}')
                yield 'show_post', {'language': language, 'path': path}

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
