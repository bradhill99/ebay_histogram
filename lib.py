import requests
import os
import base64
import json
import sys

def get_token():
    '''
        return token
        scope is a list that eBay support 
    '''
    encode_str = '{}:{}'.format(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
    encode = base64.b64encode(encode_str.encode())
    r = requests.post(
        os.environ['TOKEN_URL'], 
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(encode.decode())
        },
        data={
            'grant_type': 'client_credentials', 
            'scope': 'https://api.ebay.com/oauth/api_scope'
        })

    if r.status_code != 200:
        return ""

    return json.loads(r.text)['access_token']

def query_completed_items(access_token, start_date, end_date, pagination = 1):
    params = {
        'OPERATION-NAME':'findCompletedItems',
        'SERVICE-VERSION':'1.7.0',
        'SECURITY-APPNAME':os.environ['CLIENT_ID'],
        'RESPONSE-DATA-FORMAT':'JSON',
        'keywords':'hobby box -break',
        'categoryId':'212',
        'itemFilter(0).name':'SoldItemsOnly',
        'itemFilter(0).value':'true',
        'itemFilter(1).name':'EndTimeFrom',
        'itemFilter(1).value':start_date,
        'itemFilter(2).name':'EndTimeTo',
        'itemFilter(2).value':end_date,
        'sortOrder':'EndTimeSoonest',
        'paginationInput.pageNumber':pagination,   
    }
    r = requests.get(
        os.environ['FINDING_API'],
        params,
        headers={
            "Authorization": "Bearer {}".format(access_token)
        },
    )

    if r.status_code != 200:
        return ""

    r_dict = json.loads(r.text)
    # should improve error handling for this part, findCompletedItemsResponse and searchResult may be empty
    if 'item' in r_dict['findCompletedItemsResponse'][0]['searchResult'][0]:
        item = r_dict['findCompletedItemsResponse'][0]['searchResult'][0]['item']
    else:
        return ""

    total_page = int(r_dict['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0])
    if pagination < total_page:
        pagination += 1
        result = query_completed_items(access_token, start_date, end_date, pagination)
        item.append(result)
        return item
    else:
        return item

def get_query_time_range(start_date):
    from datetime import datetime
    from datetime import timedelta

    date_time_obj = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = date_time_obj.strftime("%Y-%m-%dT00:00:00.000Z")
    end_date = (date_time_obj+timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000Z")
    return (start_date, end_date)

def save_result(result, start_date):
    result_file = open('{}.txt'.format(start_date), 'w')
    for item in result:
        result_file.write('{}\n'.format(json.dumps(item)))

    result_file.close()

'''
Usage FINDING_API=<> CLIENT_ID=<> CLIENT_SECRET=<> TOKEN_URL=<> lib.py <YYYY-MM-DD>
'''
if __name__ == "__main__":
    token = get_token()
    (start_date, end_date) = get_query_time_range(sys.argv[1])
    result = query_completed_items(token, start_date, end_date)
    save_result(result, sys.argv[1])
