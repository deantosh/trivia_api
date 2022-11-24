# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.



## Testing

If you add another functionality, Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### API REFERENCES

## Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at 
the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
{
    "sucess": False,
    "error": 400,
    "message": "Invalid request"
}

The API will return four error types when requests fail:

  i. 400: Invalid request
 ii. 404: Resource Not Found
iii. 405: Method Not Allowed
 iv. 422: Not Processable

## Endpoints

# GET  /categories

General
  i. Returns a list of category objects, sucess value and total categories

Sample: `curl http://127.0.0.1:5000/categories`

Sample Response:

{
"categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    }
  ],
"success": true,
"total_categories": 3
}

# GET  /questions

General
  i. Returns a list of category objects, question objects, sucess value, total categories and total questions.
 ii. Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: `curl http://127.0.0.1:5000/questions`

Sample Response:

{
"categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    }
  ],
"current_category": [
  3,
  2,
  1
],
"questions": [
    {
      "answer": "Apollo 13",
      "category": 3,
      "difficulty": 4,
      "id": 1,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 2,
      "difficulty": 5,
      "id": 2,
      "question": "Which actor did Author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 1,
      "difficulty": 4,
      "id": 3,
      "question": "Whose autobiography is entitled 'I know why the caged bird sings'?"
    },
    
  ],
"success": true,
"total_categories": 3,
"total_questions": 3
}

# POST /questions

General:
  i. Creates a new question using the submitted question, answer, difficulty and category. Return the id of the created question, success mesage. Question details are updated at the frontend.
 ii. Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which is the largest lake in Africa?", "answer": "Lake Victoria", "category":"2", "difficulty":"4"}'`

Sample Response:

{
  "success": true,
  "created": 14
}

# DELETE  /questions/{question_id}

General:
  i. Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value    Then updates the frontend.
 ii. Sample: `curl -X DELETE http://127.0.0.1:5000/questions/10`

Sample Response:

{
    "question_deleted": 10,
    "success": True
}

# POST /questions/search

General:
  i. Get questions based on the search term. Returns success value, questions obtained from search, total questions, search term and current categories.
  ii. Sample: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d "{\"searchTerm\": \"penicillin\"}"`

Sample Response:
{
  "current_categories": [
    1
  ],
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "search": "Penicilin",
  "success": true,
  "total_questions": 1
}

# GET /categories/category_id/questions

General:
  i. Get questions of a specific category.  Returns success value, total questions, list of questions and current category.
 ii. Sample: `curl -X GET http://127.0.0.1:5000/categories/1/questions`

Sample Response:
{
  "current_category": 1,
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category":,
      "difficulty":,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": True,
  "total_questions": 2
}

# POST /quizzes

General:
 i. Get one random question determined by the quiz_category and not in the previous_questions array. To have one without category, quiz_category need to be 0. The response have: success value, question selected and previous_question array.

Sample: `curl -X POST http://localhost:5000/quizzes -H 'Content-type:application/json' -d "{\"previous_questions\":[10,11],\"quiz_category\":1}"`

Sample Response:

{
  "current_categories": [
    1
  ],
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 2
}

General:
## Deployment 
N/A

## Authors
Yours truly, Deantosh Daiddoh

## Acknowledgements
The awesome team of audacity  and Coach Caryn, soon to be a full stack developer! 


