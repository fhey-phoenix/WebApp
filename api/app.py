import logging
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS
from privategpt.utils import private_gpt_chain
# from scraper.utils import hr_gpt_chain
# from gpt4vision.utils import gpt4vision
# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/privategptstream', methods=['POST'])
def privategptstream():
    """
    Endpoint to generate tokens based on a prompt for Azure GPT

    Returns:
        Response: Response object containing generated tokens.

    """
    user_question = request.get_json()['user_question']

    def generate_tokens():
        g = private_gpt_chain(user_question)
        try:
            while True:
                token = next(g)
                yield token
        except StopIteration:
            pass
    return Response(stream_with_context(generate_tokens()), mimetype='text/event-stream')

@app.route('/test', methods=['GET'])
def test():
    """
    Endpoint to generate tokens based on a prompt for Azure GPT

    Returns:
        Response: Response object containing generated tokens.

    """

    def generate_tokens():
        g = private_gpt_chain("Write a 10 word poem about the ocean.")
        try:
            while True:
                token = next(g)
                yield token
        except StopIteration:
            pass
    return Response(stream_with_context(generate_tokens()), mimetype='text/event-stream')

# @app.route('/scrapergptstream', methods=['GET'])
# def hrgptstream():
#     """
#     Endpoint to generate tokens based on a prompt for HR Documents

#     Returns:
#         Response: Response object containing generated tokens.

#     """
#     prompt = request.args.get('prompt', "What are our holidays for 2024?")

#     def generate_tokens():
#         g = hr_gpt_chain(prompt)
#         try:
#             while True:
#                 token = next(g)
#                 yield token
#         except StopIteration:
#             pass
#     return Response(stream_with_context(generate_tokens()), mimetype='text/event-stream')

# @app.route('/gptvision', methods=['POST'])
# def gptvision():
#     """
#     Endpoint to generate tokens based on a prompt for Azure GPT Vision

#     Returns:
#         Response: Response object containing generated tokens.

#     """
#     prompt = request.json.get('prompt', "Describe the image")
#     img64 = request.json.get('img64', "")
#     def generate_tokens():
#         g = gpt4vision(prompt, img64)
#         try:
#             while True:
#                 token = next(g)
#                 yield token
#         except StopIteration:
#             pass
#     return Response(stream_with_context(generate_tokens()), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
