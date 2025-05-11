from flask import Flask, jsonify, render_template, send_from_directory
from builder import build_and_serve

app = Flask(__name__, static_folder='static', template_folder='templates')
PROJECTS = []

@app.route('/')
def home():
    return render_template('main.html', projects=PROJECTS)

@app.route('/new')
def new_project():
    PROJECTS.append('NewProject')
    return jsonify({'status': 'created', 'name': 'NewProject'})

@app.route('/build', methods=['POST'])
def build():
    try:
        ipa_url = build_and_serve()
        return jsonify({'success': True, 'ipa_url': ipa_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/docs/<path:filename>')
def docs_files(filename):
    return send_from_directory('docs', filename)

if __name__ == '__main__':
    app.run()
