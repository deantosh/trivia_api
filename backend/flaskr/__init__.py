import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 2


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Header", "Content-Type,Authorization,true"
            )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
            )
        return response

    # ------------------------------------------- #
    # Get list of all categoories API
    # ------------------------------------------- #
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        try:
            category_list = Category.query.all()

            # Format category_list
            categories = [category.format() for category in category_list]

            if len(categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': categories,
                'total_categories': len(categories)
            })

        except:
            abort(422)

    # -------------------------------------------------------------#
    # Get list of all questions API
    # -------------------------------------------------------------#
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        try:
            # Get list of questions and categories
            question_list = Question.query.order_by(Question.id).all()
            category_list = Category.query.all()

            # Server-side pagination using -- limit & offset method
            items_limit = request.args.get('limit', 10, type=int)
            selected_page = request.args.get('page', 1, type=int)
            current_index = selected_page - 1

            questions = \
                Question.query.order_by(
                    Question.id
                ).limit(items_limit).offset(current_index * items_limit).all()

            # Format the list
            selected_questions = [question.format() for question in questions]
            formatted_categories = [
                category.format() for category in category_list
                ]

            # If there are no categories and questions raise an exception (404)
            if len(formatted_categories) == 0 or len(selected_questions) == 0:
                abort(404)

            # Get the current categories of questions in that page
            current_categories = []

            for question in selected_questions:

                category = question['category']

                if not (category in current_categories):

                    current_categories.append(category)

            return jsonify({
                'success': True,
                'questions': selected_questions,
                'total_questions': len(question_list),
                'current_category': current_categories,
                'categories': formatted_categories,
                'total_categories': len(category_list)
            })
        except:
            abort(404)

    # -------------------------------------------------------------- #
    # Delete questions API
    # -------------------------------------------------------------- #
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        # Get specific question to be deleted
        question = Question.query.filter(
            Question.id == question_id
            ).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'question_deleted': question_id
            })

        except:
            abort(405)

    # ------------------------------------------------------------ #
    # POST questions API
    # ------------------------------------------------------------ #
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            # Get data from json
            body = request.get_json()

            # Question details to be created
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            # Create question object
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category
            )

            # Insert into the questions table
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except:
            abort(422)

    # ----------------------------------------------------- #
    # POST - get questions based on a search term API
    # ----------------------------------------------------- #
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        search = "%{}%".format(search_term.replace(" ", "\ "))

        # get search results
        search_results = Question.query.filter(
            Question.question.ilike(search)
            ).all()

        # Format the questions in search results
        formatted_questions = [
            question.format() for question in search_results
            ]

        if len(formatted_questions) == 0:
            abort(404)

        try:
            # Get the categories of the questions obtained in search result
            current_categories = []

            for question in formatted_questions:
                category = question['category']

                # If category does not exist add it to list
                if not (category in current_categories):
                    current_categories.append(category)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'search': search_term,
                'current_categories': current_categories
            })

        except:
            abort(422)

    # ------------------------------------------------------ #
    # GET - questions based on category API
    # ------------------------------------------------------ #
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        # Get list of categories
        category_list = Category.query.all()

        try:

            # Server-side pagination using -- limit & offset method
            items_limit = request.args.get('limit', 10, type=int)
            selected_page = request.args.get('page', 1, type=int)
            current_index = selected_page - 1

            questions = \
                Question.query.filter(
                    Question.category == category_id
                ).limit(items_limit).offset(current_index * items_limit).all()

            # Format questions
            selected_questions = [question.format() for question in questions]

            if len(selected_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': selected_questions,
                'total_questions': len(selected_questions),
                'current_category': category_id
            })

        except:
            abort(404)

    # --------------------------------------------------- #
    # POST - get questions to play the quiz API
    # --------------------------------------------------- #
    @app.route('/quizzes', methods=['POST'])
    def post_quiz_questions():

        try:
            quiz_result = request.get_json()

            # Get list of categories and previous quiz questions
            quiz_category = quiz_result.get('quiz_category')
            previous_questions = quiz_result.get('previous_questions')

            question = Question.query
            question = question.filter(~Question.id.in_(previous_questions))

            if quiz_category != 0:
                question = question.filter(Question.category == quiz_category)

            questions_random = question.order_by(func.random()).first()

            if not questions_random:
                return (jsonify({
                    'success': True,
                    'previous_question': len(previous_questions)
                }))

            return jsonify({
                'success': True,
                'question': questions_random.format(),
                'previous_question': previous_questions
            })
        except:
            abort(422)

    # --------------------------------- #
    # Error Handler
    # --------------------------------- #
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "internal server error"
        }), 500

    return app

