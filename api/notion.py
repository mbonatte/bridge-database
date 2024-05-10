import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from the .env file

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

HEADERS = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

def clean_data(result):
    return {
        'name': result['properties']['Name']['title'][0]['text']['content'],
        'id': result['id'],
        'latitude': result['properties']['latitude']['number'],
        'longitude': result['properties']['longitude']['number'],
    }

def fetch_notion_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        return list(map(clean_data, response.json()['results']))
    else:
        return response.status_code, response.text
        
def get_bridge_photos(blocks, content):
    images = []

    # Function to recursively search for the 'Photos' section under 'Collapse'
    def recurse_through_blocks(blocks, in_collapse=False):
        for block in blocks:
            if block['content'] == content:
                if 'children' in block:
                    recurse_through_blocks(block['children'], in_collapse = True)
            elif 'children' in block and in_collapse:
                recurse_through_blocks(block['children'], in_collapse)
            elif block['type'] == 'image' and in_collapse:
                images.append(block['content'])

    recurse_through_blocks(blocks)
    return images

def fetch_bridge_database(bridge_id):
    contents = fetch_all_nested_blocks(bridge_id)
    info = {}
    for content in contents:
        if content['type'] == 'code':
            info['bridge'] = content['content']
    
    info['general_photos'] = get_bridge_photos(contents, 'General')
    info['collapse_photos'] = get_bridge_photos(contents, 'Collapse')
    
    return info
    
def fetch_block_children(block_id, page_size = 100):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size={page_size}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # This returns the page properties and metadata
    else:
        return response.status_code, response.text

def fetch_all_nested_blocks(block_id):
    data = []
    children = fetch_block_children(block_id)
    if 'results' in children:
        for child in children['results']:
            block_content = {
                'type': child['type'],
                'content': extract_content(child)
            }
            if child.get('has_children', False):
                block_content['children'] = fetch_all_nested_blocks(child['id'])
            data.append(block_content)
    return data

def extract_content(block):
    block_type = block['type']
    content = block[block_type]
    if block_type == 'paragraph':
        return ' '.join([text['plain_text'] for text in content['rich_text']])
    elif 'heading' in block_type:
        return content['rich_text'][0]['plain_text'] if content['rich_text'] else ''
    if block_type == 'code':
        return json.loads(content['rich_text'][0]['text']['content'])
    elif block_type == 'image':
        return content['file']['url']
    return ""