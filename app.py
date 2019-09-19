from flask import Flask, render_template
import requests

# change <TOKEN> here
TOKEN = "CDE08aXRjayPXXXHrQ-P63R-x0vOPKVl6EQ0CImUtgBII064DilNWrhsazGRnpNr"

# book-keeping some addresses
URL = "http://density.adicu.com/latest"
APPENDIX = "?auth_token=" + TOKEN
INFO_URL = "https://density.adicu.com/docs/building_info"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/information/<building>')
def show_occupancy(building):
    # show the occupancy of the building with given name
    parent = building.lower()
    r_info = requests.get(INFO_URL)
    list_of_entries = r_info.json()["data"] # obtain a list of libraries
    parent_id = 0
    # search for the given parent in the list
    for i in list_of_entries:
        if (i["parent_name"].lower().replace(' ','_') == parent):
            parent_id = i["parent_id"]
            break
    # return message for invalid name
    if parent_id == 0:
        return "invalid building name"
    # inquire data regarding the given parent
    url_request = ''.join([URL,'/building/',str(parent_id),APPENDIX])
    r = requests.get(url_request)
    response = []
    # for each group under the parent, display its occupancy
    for i in r.json()["data"]:
        response.append('{} is {}% full'.format(i['group_name'],i['percent_full']))
    final_response = '\n'.join(response)
    final_response = "<pre>{}</pre>".format(final_response)
    return final_response

@app.route('/information/<int:rank>')
def show_building(rank):
    # show the buildings within the given rank, the rank is an integer
    r_info = requests.get(INFO_URL)
    list_of_entries = r_info.json()["data"] # obtain a list of libraries
    list_of_responses = []
    for i in list_of_entries:
        # for each library group, obtain its occupancy, and store it in a list
        url_request = ''.join([URL,'/group/',str(i['group_id']),APPENDIX])
        r = requests.get(url_request)
        list_of_responses += r.json()["data"]
    # return the entires upto given rank
    sorted_entries = sorted(list_of_responses, key=lambda i:i['percent_full'])
    response = []
    for i in sorted_entries[:rank]:
        response.append('{} is {}% full'.format(i['group_name'],i['percent_full']))
    final_response = '\n'.join(response)
    final_response = "<pre>{}</pre>".format(final_response)
    return final_response

if __name__ == '__main__':
    app.run()
