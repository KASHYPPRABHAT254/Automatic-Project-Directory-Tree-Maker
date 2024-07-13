import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def fetch_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None

def parse_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    return links

def web_tree_to_xml(url, parent_node, depth=2):
    if depth == 0 or url in visited_urls:
        return
    
    visited_urls.add(url)
    html_content = fetch_website_content(url)
    if html_content:
        links = parse_links(html_content, url)
        current_node = ET.SubElement(parent_node, 'website', url=url)

        for link in links:
            link_node = ET.SubElement(current_node, 'link', url=link)
            web_tree_to_xml(link, link_node, depth - 1)

def tree_to_xml(directory, parent_node):
    root = os.path.abspath(directory)
    files = []
    dirs = []

    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isfile(path):
            files.append(path)
        if os.path.isdir(path):
            dirs.append(path)

    current_node = ET.SubElement(parent_node, 'directory', name=os.path.basename(root))

    for file_path in files:
        ET.SubElement(current_node, 'file', name=os.path.basename(file_path))

    for dir_path in dirs:
        tree_to_xml(dir_path, current_node)
