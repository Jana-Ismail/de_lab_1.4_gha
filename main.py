import json
import os
import pandas as pd
import requests
from requests.exceptions import HTTPError

def create_user(user):
    url = 'https://developyr-api.azurewebsites.net/api/auth'
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
        with open(file_path, 'a'):
            pass

def main():
    # token = get_token()
    # need to put user data in .env file, rather than hard coding
    user = {
        'username': 'admin',
        'password': 'password123'
    }

    user_response = create_user(user)
    # print(user_response)

    headers = {'Authorization': f'Bearer {user_response['token']}'}

    people_response = get_people(headers)
    # print(people_response)

    people_with_query_params = get_people(headers, 2, 10)
    # print(people_with_query_params)

    total = people_response['total_items']

    file_path = './data/people_from_azure_api.json'
    load_people_to_json_file(headers, total, file_path)



if __name__ == "__main__":
    main()












# with open(file_path, 'rb+') as f:
#     # replace last ']' character with ','
#     # in the existing .json file
    
#     # Move to the end of the file and read backwards to find the last char
#     f.seek(-1, 2) # -1 argument goes to last byte, 2 seeks the end of the file [0 => beginning of file, 1=>current position of the file pointer]
#     last_char = f.read(1) # read the byte that .seek() found

#     if last_char == b']':
#         f.seek(-1, 2) # move back to overwrite
#         f.write(b',')