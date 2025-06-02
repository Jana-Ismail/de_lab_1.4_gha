## Lab 1.4

### Introduction
The purpose of this lab is to learn how to access data from an API using pagination in Python. 

### Part 1
Using the same API from Lab 1.3, get a token and authenticate to the API. Verify this by hitting `/people`. Do this in Postman first.
POST request to: https://developyr-api.azurewebsites.net/api/auth
response:

{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzQ4NjIxODc3fQ.MCAesV6oXTlU57QzzdudhWStifZERnCkoz8tLqO62us",
    "expires_at": "2025-05-30T16:17:57.578687Z"
}

GET request to: https://developyr-api.azurewebsites.net/api/people

### Part 2
Add query string params `offset` and `limit` to the call in order to get a subset of the results back.  Note here that the API is set to a max number of **50** results. Do this in Postman first.

GET: https://developyr-api.azurewebsites.net/api/people?offset=4&limit=10

{
    "offset": 4,
    "limit": 10,
    "total_items": 50,
    "data": [
        {
            "first_name": "George",
            "last_name": "Barnett",
            "email": "littlekatherine@example.org",
            "address": "PSC 0665, Box 3648\nAPO AP 40416"
        },
        {
            "first_name": "Robert",
            "last_name": "Bates",
            "email": "thompsoneric@example.org",
            "address": "96575 Alvarez Tunnel Suite 927\nPhillipsville, WI 24830"
        },
        {
            "first_name": "Vicki",
            "last_name": "Black",
            "email": "ekerr@example.com",
            "address": "358 Denise Valleys Apt. 959\nEast Timothy, TX 89075"
        },
        {
            "first_name": "Robert",
            "last_name": "Boyle",
            "email": "dbanks@example.net",
            "address": "3516 Diaz Hill Suite 644\nSouth Ashley, ID 67141"
        },
        {
            "first_name": "William",
            "last_name": "Brady",
            "email": "fergusoncarrie@example.com",
            "address": "4189 Madison Glens Suite 206\nLake Vickiborough, TN 20792"
        },
        {
            "first_name": "Aaron",
            "last_name": "Castillo",
            "email": "roy72@example.com",
            "address": "9595 Gary Port\nLarafort, TN 04209"
        },
        {
            "first_name": "Jose",
            "last_name": "Clark",
            "email": "zblankenship@example.net",
            "address": "151 Christopher Mission\nEast Richardfurt, WV 99208"
        },
        {
            "first_name": "Cody",
            "last_name": "Cochran",
            "email": "jennifer14@example.net",
            "address": "554 Williams Mountain\nSouth Anthonyville, SD 39567"
        },
        {
            "first_name": "Andres",
            "last_name": "Cox",
            "email": "wyoung@example.org",
            "address": "5983 Torres Ramp Apt. 049\nSouth Ashleybury, MO 55441"
        },
        {
            "first_name": "Elizabeth",
            "last_name": "David",
            "email": "smithdouglas@example.com",
            "address": "19721 Drew Key\nNew Donaldport, NH 05690"
        }
    ]
}

### Part 3
You have now proven that the API is accessible. Checking your code first in Postman helps you determine if it is the API that is not working versus your code.

Now repeat Parts 1 and 2 using Python. 

### Part 4
Once can read data from the API using Python, save the data to a `.json` file 10 records at a time. Do not hold any more than 10 records in memory at once. 

### Part 5 
Instead of writing this to a json file, reformat to write to a `.csv` file still holding only 10 records at a time in memory. 
