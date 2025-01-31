import json

def get_faq_data():
    # Example of pulling data from a JSON file or an external CMS
    with open('data/faq_data.json', 'r') as file:
        data = json.load(file)
    return data
