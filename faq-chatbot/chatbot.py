from nlp_processing import process_query, generate_response

def get_response(user_query):
    processed_query = process_query(user_query)
    response = generate_response(processed_query)
    return response
