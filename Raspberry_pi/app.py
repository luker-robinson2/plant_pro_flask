from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def get_image():
    # use the camera to to take pictures
    pass

def get_moisture_level():
    # use moisture sensor to get moisture
    pass

import requests

def make_request(url, method="GET", params=None, data=None, headers=None):
    """
    Makes a GET or POST request and returns the JSON response.

    Parameters:
        url (str): The URL to make the request to.
        method (str): The HTTP method to use, "GET" or "POST". Defaults to "GET".
        params (dict): Query parameters for the request. Defaults to None.
        data (dict): Data to send in the body of the request for POST. Defaults to None.
        headers (dict): Headers to include in the request. Defaults to None.

    Returns:
        dict: The JSON response from the server.
    """
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, data=data, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method. Use 'GET' or 'POST'.")

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Return the JSON content
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response: {e}")
        return None


url = "https://jsonplaceholder.typicode.com/posts"
response = make_request(url, method="GET", params={"userId": 1})
print(response)
