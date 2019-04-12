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

def do_query(access_token, start_date, end_date, pagination):
    params = {
        'OPERATION-NAME':'findCompletedItems',
        'SERVICE-VERSION':'1.7.0',
        'SECURITY-APPNAME':os.environ['CLIENT_ID'],
        'RESPONSE-DATA-FORMAT':'JSON',
        'categoryId':'212',
        'itemFilter(0).name':'SoldItemsOnly',
        'itemFilter(0).value':'true',
        'itemFilter(1).name':'EndTimeFrom',
        'itemFilter(1).value':start_date,
        'itemFilter(2).name':'EndTimeTo',
        'itemFilter(2).value':end_date,
        'sortOrder':'EndTimeSoonest',
        'paginationInput.pageNumber':pagination,
        'aspectFilter(0).aspectName':'Product',
        'aspectFilter(0).aspectValueName':'Box'
    }
    r = requests.get(
        os.environ['FINDING_API'],
        params,
        headers={
            "Authorization": "Bearer {}".format(access_token)
        },
    )

    if r.status_code != 200:
        raise ValueError('http error, status code={}'.format(r.status_code))

    r_dict = json.loads(r.text)
    try:
        r_dict['findCompletedItemsResponse'][0]['searchResult'][0]['item'] = post_process(r_dict['findCompletedItemsResponse'][0]['searchResult'][0]['item'])
    except:
        print(r.text)
        raise ValueError('key exception')

    print("item size={}".format(len(r_dict['findCompletedItemsResponse'][0]['searchResult'][0]['item'])))
    return r_dict

def post_process(items):
    # remove item with title has "break"
    # add @timestamp key
    filter_items = [ item for item in items if "break" not in item['title'][0].lower() ]
    add_timestamp_field(filter_items)
    return filter_items

def add_timestamp_field(items):
    for item in items:
        item['@timestamp'] = item['listingInfo'][0]['endTime'][0]

def query_completed_items(access_token, start_date, end_date):
    pagination = 1
    # total_items = list()
    try:
        # get first query and number of pages
        result = do_query(access_token, start_date, end_date, pagination)
        total_page = int(result['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0])
        # total_items.extend(result['findCompletedItemsResponse'][0]['searchResult'][0]['item'])
        save_result(result['findCompletedItemsResponse'][0]['searchResult'][0]['item'])
        print("currnt page={}, total pages={}".format(pagination, total_page))

        while pagination < total_page:
            pagination += 1
            result = do_query(access_token, start_date, end_date, pagination)
            save_result(result['findCompletedItemsResponse'][0]['searchResult'][0]['item'])
            print("currnt page={}, total pages={}".format(pagination, total_page))
            # total_items.extend(result['findCompletedItemsResponse'][0]['searchResult'][0]['item'])
    except Exception as e:
        print('got exception, break the loop:{}'.format(e))

    # print("total_items size={}".format(len(total_items)))
    # return total_items

def get_query_time_range(start_date):
    from datetime import datetime
    from datetime import timedelta

    date_time_obj = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = date_time_obj.strftime("%Y-%m-%dT00:00:00.000Z")
    end_date = (date_time_obj+timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000Z")
    return (start_date, end_date)

def save_result(result):
    start_date = sys.argv[1]
    result_file = open('{}.txt'.format(start_date), 'a')
    for item in result:
        result_file.write('{}\n'.format(json.dumps(item)))

    result_file.close()

'''
Usage FINDING_API=<> CLIENT_ID=<> CLIENT_SECRET=<> TOKEN_URL=<> lib.py <YYYY-MM-DD>
'''
if __name__ == "__main__":
    token = get_token()
    (start_date, end_date) = get_query_time_range(sys.argv[1])
    query_completed_items(token, start_date, end_date)
    # save_result(result, sys.argv[1])
