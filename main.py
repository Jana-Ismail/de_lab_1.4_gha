import json
import os
import requests
import csv
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()

def main():
    # token = get_token()
    user = {
        'username': os.getenv('API_USERNAME'),
        'password': os.getenv('API_PASSWORD')
    }

    user_response = create_user(user)

    headers = {'Authorization': f'Bearer {user_response['token']}'}
    people_response = get_people(headers)

    people_with_query_params = get_people(headers, 2, 10)

    total = people_response['total_items']

    json_file_path = './data/people_from_azure_api.json'
    load_people_to_json_file(headers, total, json_file_path)

    csv_file_path = './data/people_from_azure_api.csv'
    load_people_to_csv(headers, total, csv_file_path)

def create_user(user):
    url = f'{os.getenv('BASE_URL')}/auth'
    try:
        response = requests.post(url, json=user)

        return response.json()
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')

def get_people(headers, limit=None, offset=None):
    url = 'https://developyr-api.azurewebsites.net/api/people'
    query_params = None
    
    if limit and offset:
        query_params={
            'limit': limit,
            'offset': offset
        }

    try:
        response = requests.get(url, headers=headers, params=query_params)

        return response.json()
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')

def load_people_to_json_file(headers, total, file_path):
    limit=10
    offset=0

    while offset < total:
        
        if not os.path.exists(file_path):
            response = get_people(headers, limit, offset)
            people = response['data']
            
            with open(file_path, 'w') as f: 
                json.dump(people, f)
        else:
            with open(file_path, 'rb+') as f:
                f.seek(-1, 2) # Go to end of file and find last byte
                last_char = f.read(1) # Read that byte

                # Check if that byte is a ']'
                if last_char == b']':
                    # Go to end of file and find last byte again
                    f.seek(-1, 2)
                    # Overwrite the ']' with a ','
                    f.write(b',')

                response = get_people(headers, limit, offset)
                people = response['data']

                people_json = json.dumps(people)
                people_json = people_json[1:] # Slice off '[' char
            
                with open(file_path, 'a') as f:
                    f.write(people_json)
        
            offset += 10
            
        if offset >= total:
            with open(file_path, 'rb+') as f:
                f.seek(-2, 2)
                second_to_last_char = f.read(1)
                
                f.seek(-1, 2)
                last_char = f.read(1)
                
                if second_to_last_char == ',' and last_char == b' ':
                    f.seek(-1, 2)
                    f.write(b'')
                    
                    f.seek(-1, 2)
                    f.write(b']')

def load_people_to_csv(headers, total, file_path):
    limit=10
    offset=0

    while offset < total:
        response = get_people(headers, limit, offset)
        people = response['data']

        if not os.path.exists(file_path):
            header = people[0].keys()

            # Use DictWriter to write to CSV
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                writer.writeheader()
                for person_row in people:
                    escaped_row = {key: value.replace('\n', '\\n') if isinstance(value, str) else value for key, value in person_row.items()}
                    writer.writerow(escaped_row)
            
        else:
            with open(file_path, 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                for person_row in people:
                    escaped_row = {key: value.replace('\n', '\\n') if isinstance(value, str) else value for key, value in person_row.items()}
                    writer.writerow(escaped_row)
                
        offset += 10

if __name__ == "__main__":
    main()
