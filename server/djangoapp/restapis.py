import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("An error occurred while making GET request. ")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")

    # Retrieving the response status code and content
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)

    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload
    print("Payload: ", json_obj, ". Params: ", kwargs)
    print("POST to {} ".format(url))
    # print(json_payload["review"])
    try:
        response = requests.post(
            url, headers={'Content-Type': 'application/json'}, json=json_obj, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], short_name=dealer_doc["short_name"], st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], short_name=dealer_doc["short_name"], st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    # print(json_result)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            results.append(review_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    api_key = "rMr5it11GMlIL5g6Xz3q6b4xeDWAzBtQZJy11daNf3gU"
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/59f69556-706c-479c-96e7-7ad112731400"
    text = review
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=version,
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    try:
        response = natural_language_understanding.analyze(text=text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))
        # sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"
    # print(sentiment_score)
    # print(sentiment_label)
    sentimentresult = sentiment_label

    return sentimentresult


