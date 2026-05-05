import requests

URL = "http://localhost:8000/notes/"  ### Website holen

def test_get_all_notes():
    response = requests.get(URL)
    if response.status_code == 200:
       print("GET / - successful")
    else:
        print("GET / - failed")


def create_notes():
   for i in range(1, 6):
      payload = {
         "title": f"title {i}",
         "content": f"content {i}",
         "category": f"category {i % 2}" # Alternating categories: category 0 and category 1
         "tags": [f"tag{i}", f"tag{i+1}"] # Example tags
        }













