import os
import json
import requests
import csv

def auth():
    return os.environ.get("BEARER_TOKEN")

#URL TO ACCESS 100 MOST RECENT TWEETS WITH THE WORDS "CLIMATE" AND "CHANGE"
def create_url():

    url = "https://api.twitter.com/2/tweets/search/recent?query=(carbon) -is:retweet -is:reply -has:links " \
          "-has:media -has:images -has:videos lang:en&max_results=100"

    return url

#BE SURE YOUR AUTHORIZATION INFORMATION IS IN THE ENVIRONMENT VARIABLE "BEARER_TOKEN"
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    bearer_token = auth()
    url = create_url()

    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)

    carbon = []
    carbon_and_covid = []
    count = 0

    #BEFORE RUNNING THIS CODE, CREATE AN EMPTY CSV FILE CALLED "climatechange.csv"
    #THE FOLLOWING CODE WILL WRITE THE PULLED TWEETS TO THAT FILE ON YOUR COMPUTER (SAME DIRECTORY AS THIS PYTHON FILE)
    with open("carbon.csv", "w") as carboncsv:
        carbon_writer = csv.writer(carboncsv)

        data_section = json_response["data"]

        for elem in data_section:
            count += 1
            text_section = str.lower(elem["text"])
            carbon_writer.writerow([text_section])

            if "carbon" in text_section:
                carbon.append(elem)
            else:
                print(elem)

            if "covid" in text_section or "corona" in text_section or "pandemic" in text_section:
                carbon_and_covid.append(elem)

    #PRINTS # OF TWEETS (USUALLY 100, BUT CAN VARY SLIGHTLY)
    print("# of carbon Tweets: ", len(carbon))
    #PRINTS # OF TWEETS THAT INCLUDED COVID REFERENCES AS DEFINED ON LINE 57c
    print("# of carbon Tweets that include COVID references: ", len(carbon_and_covid))


if __name__ == "__main__":
    main()