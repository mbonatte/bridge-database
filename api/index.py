import json

from flask import Flask, jsonify, request, render_template

from api.notion import fetch_notion_database, fetch_bridge_database

app = Flask(__name__)


def get_bridge_by_name(bridge_name):
    for bridge in bridges_data['bridges']:
        if bridge['general_info']['bridge_name'] == bridge_name:
            return bridge
    return None


@app.route('/')
def index():
    return render_template('index.html');

@app.route('/bridges/names', methods=['GET'])
def get_bridge_names():
    bridge_names = fetch_notion_database()
    return jsonify(bridge_names)

@app.route('/bridges/details', methods=['GET'])
def get_bridge_details():
    # Get bridge name from query parameter
    bridge_id = request.args.get('id', default=None, type=str)
    if not bridge_id:
        return jsonify({'error': 'No bridge id provided'}), 400
    
    bridge = fetch_bridge_database(bridge_id)
    if bridge:
        return jsonify(bridge['bridge'])        
    
    return jsonify({'error': 'Bridge not found'}), 404

@app.route('/bridge/<bridge_id>')
def bridge_page(bridge_id):
    bridge = fetch_bridge_database(bridge_id)
    if bridge:
        return render_template('bridge_page.html', 
            bridge=bridge['bridge'], 
            general_photos=bridge['general_photos'], 
            collapse_photos=bridge['collapse_photos'])
    else:
        return "Bridge not found", 404

if __name__ == '__main__':
    app.run(debug=True)
