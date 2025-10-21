🧩 String Analyzer Service — HNG Backend Wizards (Stage 1)

A RESTful API that analyzes strings and stores their computed properties such as length, palindrome status, word count, unique characters, SHA-256 hash, and more.

🚀 Features

✅ Analyze and store any string
✅ Compute and return properties like:

length — total characters

is_palindrome — whether the string reads the same backward

unique_characters — count of distinct characters

word_count — number of words separated by spaces

sha256_hash — hash of the string

character_frequency_map — dictionary showing character frequency

✅ Retrieve all analyzed strings
✅ Retrieve a specific string
✅ Delete a string
✅ Filter strings using both query parameters and natural language

🏗️ Tech Stack

Python 3.12+

Django 5.2

Django REST Framework

SQLite3 (default, can switch to MySQL/PostgreSQL)

AWS for deployment

⚙️ Setup Instructions (Local)
1️⃣ Clone the repository
git clone https://github.com/GOODNEWS221/string_analyser_service.git
cd string_analyser_service

2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate    

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver


Your API will now be live at
➡️ http://127.0.0.1:8000/string

🧾 API Endpoints
1️⃣ Analyze/Create String

POST /strings

Request Body:

{
  "value": "string to analyze"
}


Response (201 Created):

{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 16,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3
    }
  },
  "created_at": "2025-10-20T10:00:00Z"
}

2️⃣ Retrieve Specific String

GET /strings/<string_value>

Response (200 OK):

{
  "id": "sha256_hash_value",
  "value": "requested string",
  "properties": { /* same as above */ },
  "created_at": "2025-10-20T10:00:00Z"
}

3️⃣ List All Strings (with Filters)

GET /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a

Example Response:

{
  "data": [ /* array of matching strings */ ],
  "count": 3,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20,
    "word_count": 2,
    "contains_character": "a"
  }
}

4️⃣ Natural Language Filter

GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

Example Response:

{
  "data": [ /* results */ ],
  "count": 2,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}

5️⃣ Delete String

DELETE /strings/<string_value>/delete

Response:
204 No Content

⚠️ Error Responses
Status Code	Meaning
400	Bad Request — Invalid or missing data
404	Not Found — String doesn’t exist
409	Conflict — String already exists
422	Unprocessable Entity — Invalid data type


🌐 Deployment (AWS)

Push code to GitHub

Connect my repo to AWS EC2 instance(Same instance I used for the stage 0 project)

Install dependencies on the server

Run migrations (python manage.py migrate)

Start the server or configure gunicorn for production





http://ec2-13-60-28-127.eu-north-1.compute.amazonaws.com/strings/



👤 Author

Goodnews Atekha
📧 goodnewsatekha@gmail.com

🌍 HNG Backend Wizards — Stage 1 Submission
