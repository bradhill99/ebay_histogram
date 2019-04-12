# Ebay API

This projec is to 
1. Show historical sale price for watch items so we can get overall sold price historgram that can help us to place a resonable bid.
2. Auto bid (may called sniper technique)

## Porject Goal
* Study Ebay API for get sold information
* Study Ebay API to bid by program
* Nice to have: Mobile App to show item sold historgram and auto bid functionality

## Ebay API
* Home page: https://developer.ebay.com
* Tutorial: https://developer.ebay.com/tools/quick-start

### Quick Start (https://developer.ebay.com/api-docs/static/make-a-call.html)
* Visit Application Keys web page: https://developer.ebay.com/my/keys
* Click **Crate a Keyset** in **Production** keyset section if none exists
* In **Production Toker** section, click **User Tokens** in **App ID** section
* Click **Get OAtuh Application Token**
* Then make http request by using application token:

HTTP component|value
--- | ---
method|      GET
URL (Production)| https://api.ebay.com/buy/browse/v1/item_summary/search?category_ids=108765&q=Beatles&filter=price:[200..500]&filter=priceCurrency:USD&limit=10
headers|Authorization: Bearer \<Application-token-value\>

### OAuth Access Token
Has two kinds of flow to get token
* Client credentials grant - If call API with read-only resources
* Authorization code grant - If call API related to user data

#### Client credentials grant flow
API signature:
```
  HTTP method:      POST
  URL (Sandbox):    https://api.sandbox.ebay.com/identity/v1/oauth2/token
  URL (Production): https://api.ebay.com/identity/v1/oauth2/token

  HTTP headers:
    Content-Type = application/x-www-form-urlencoded
    Authorization = Basic <B64 encoded of client_id:client_secret>

  Request body:
    grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope%20https://api.ebay.com/oauth/api_scope/buy.guest.order
  * scope can be a list of API scopes combined by %20
```
API scopes examples
```
https://api.ebay.com/oauth/api_scope
https://api.ebay.com/oauth/api_scope/buy.guest.order
https://api.ebay.com/oauth/api_scope/buy.item.feedS
https://api.ebay.com/oauth/api_scope/buy.marketing
```
## Category example
Category ID|      Category Name
--- | ---
215 | Football Cards
213 | Baseball Cards
214 | Basketball Cards
212 | (Sports Trading Cards)

## Search example
* Find sold items for 2018 panini contenders football for the past 3 months with catelog = football trading cards

* Find 10 listed items for cody bellinger
```
GET https://api.ebay.com/buy/browse/v1/item_summary/search?q=cody%20bellingers&limit=10
Authorization: Bearer <token>
```

## Parse json response using jq
```
# example
jq '.itemSummaries[]| {title: .title, buyingOptions:.buyingOptions}'
# find title and list type from finding API response
jq '.findCompletedItemsResponse[0].searchResult[0].item[]| {title: .title, buyingOptions:.listingInfo[0].listingType}'
```

## API endpoint
Environment | URL
--- | ---
Sandbox| https://api.ebay.com
Production | https://api.sandbox.ebay.com

## Finding API
Environment | URL
--- | ---
Sandbox| http://svcs.sandbox.ebay.com/services/search/FindingService/v1 
Production | http://svcs.ebay.com/services/search/FindingService/v1

## Ebay site
Environment | URL
--- | ---
Sandbox| https://sandbox.ebay.com
Production | https://ebay.com


