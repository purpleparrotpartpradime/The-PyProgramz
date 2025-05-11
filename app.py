from flask import Flask, jsonify, render_template, send_from_directory
from builder import build_ipa_and_package

app = Flask(__name__, static_folder='static', template_folder='templates')

# In-memory project list (demo)
PROJECTS = ['DemoApp', 'TestApp']

@app.route('/')
def home():
    return render_template('main.html', projects=PROJECTS)

@app.route('/new')
def new_project():
    # Logic to create a new project
    return 'New project creation UI (placeholder)'

@app.route('/build', methods=['POST', 'GET'])
def build():
    try:
        ipa_url = build_ipa_and_package()
        return jsonify({'success': True, 'manifest_url': ipa_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/docs/<path:filename>')
def docs_files(filename):
    return send_from_directory('docs', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
