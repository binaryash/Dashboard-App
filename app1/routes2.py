import os
import markdown
from flask import Flask, render_template, send_from_directory
from app1 import app

def apply_list_styling(html):
    # Apply styling to headings
    html = html.replace('<h1>', '<h1 class="note_main">')
    html = html.replace('<h2>', '<h2 class="note_main">')
    html = html.replace('<h3>', '<h3 class="note_main">')
    html = html.replace('<h4>', '<h4 class="note_main">')

    # Apply styling to emphasized text
    html = html.replace('<em>', '<em class="emphasized-text">')

    # Apply styling to paragraphs
    html = html.replace('<p>', '<p class="paragraph">')

    # Apply styling to code blocks
    html = html.replace('<pre>', '<pre class="code-block">')
    html = html.replace('<code>', '<code class="code">')

    # Apply styling to unordered lists (bulleted lists)
    html = html.replace('<ul>', '<ul class="unordered-list">')
    html = html.replace('<li>', '<li class="list-item">')

    # Apply styling to ordered lists (numbered lists)
    html = html.replace('<ol>', '<ol class="ordered-list">')

    return html


@app.route('/noteindex')
@app.route('/<path:directory>')
def noteindex(directory='.'):
    directory_path = os.path.join('.', directory)
    files = get_files(directory_path)
    return render_template('noteindex.html', files=files, current_directory=directory)

@app.route('/view/<path:filename>')
def view_file(filename):
    file_path = os.path.join('.', filename)
    if os.path.isfile(file_path) and file_path.endswith('.md'):
        with open(file_path, 'r') as f:
            content = f.read()
            html = markdown.markdown(content, extensions=['extra'])

            # Apply list styling
            html = apply_list_styling(html)

            return render_template('noteview.html', filename=filename, content=html)
    else:
        return "File not found or not a Markdown file."

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def get_files(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            files.append({
                'name': filename,
                'path': os.path.join(directory, filename),
                'is_directory': True
            })
        else:
            files.append({
                'name': filename,
                'path': os.path.join(directory, filename),
                'is_directory': False
            })
    return files
