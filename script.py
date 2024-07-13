import os
import sys
import xml.etree.ElementTree as ET

def tree_to_xml(directory, parent_node):
    root = os.path.abspath(directory)
    files = []
    dirs = []

    # Find list of files and directories inside the root
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isfile(path):
            files.append(path)
        if os.path.isdir(path):
            dirs.append(path)

    # Create XML element for current directory
    current_node = ET.SubElement(parent_node, 'directory', name=os.path.basename(root))

    # Add files as child elements
    for file_path in files:
        ET.SubElement(current_node, 'file', name=os.path.basename(file_path))

    # Recursively add directories as child elements
    for dir_path in dirs:
        tree_to_xml(dir_path, current_node)

def main():
    if len(sys.argv) == 1:
        print("Please provide a directory path.")
        return
    
    directory = sys.argv[1]
    
    # Create XML structure
    root = ET.Element('directory_tree')
    tree_to_xml(directory, root)

    # Create XML tree
    tree = ET.ElementTree(root)

    # Save XML to file
    xml_file = directory.rstrip(os.sep).split(os.sep)[-1] + '_tree.xml'  # Create a filename based on the directory name
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    print(f"Directory tree saved to {xml_file}")

if __name__ == '__main__':
    main()
