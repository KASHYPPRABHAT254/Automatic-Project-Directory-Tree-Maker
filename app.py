from flask import Flask, send_file, request, jsonify
import xml.etree.ElementTree as ET
import os
from web_crawler import tree_to_xml, web_tree_to_xml

app = Flask(__name__)

@app.route('/generate_xml', methods=['GET'])
def generate_xml():
    directory = request.args.get('directory')
    url = request.args.get('url')
    depth = int(request.args.get('depth', 2))

    root = ET.Element('directory_tree')

    if directory:
        if not os.path.isdir(directory):
            return jsonify({"error": f"{directory} is not a valid directory path."}), 400
        tree_to_xml(directory, root)
    elif url:
        web_tree_to_xml(url, root, depth)
    else:
        return jsonify({"error": "Please provide a directory or URL"}), 400

    tree = ET.ElementTree(root)
    xml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'directory_tree.xml')
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    return send_file(xml_file)

if __name__ == '__main__':
    app.run(debug=True)
