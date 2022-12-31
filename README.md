# url-shortener

## supports the following API calls:

``` 
curl -X POST "http://127.0.0.1:8000/create" -H "Content-Type: application/json" -d "{\"url\": \"https://ravkavonline.co.il\"}" 

```
pay attention to the data [-d] syntax, you must escape the double-quotes in order to send valid JSON payload (such that maintains the key and value wrapped in double-quotes) 

examples of bad data [-d] syntax: 

* ```curl -X POST "http://127.0.0.1:8000/create/" -H "Content-Type: application/json" -d '{"url": "https://ravkavonline.co.il"}'``` results in an error ```curl: (3) unmatched close brace/bracket in URL position 27:
https://ravkavonline.co.il}'```. In this case, the issue is likely caused by the single quotes `'` around the JSON payload and the space char between the `:` and the beginning of the URL. The single quotes are being interpreted as part of the URL, causing the error message. 

* ``` curl -X POST "http://127.0.0.1:8000/create/" -H "Content-Type: application/json" -d "{"url": "https://ravkavonline.co.il"}" ``` request body is received at the server side (after decoding) as: ```{url: https://ravkavonline.co.il}``` which is missing the double-quote around "url" and "https://ravkavonline.co.il". That is, the data string is not properly formatted. JSON objects must use double quotes `"` around keys and values. Passing this ```{url: https://ravkavonline.co.il}``` as input string to the `json.loads` function raises a `JSONDecodeError` since it is unable to parse the input string as a JSON object.

* Similarly to the previous example, ```curl -X POST "http://127.0.0.1:8000/create/" -H "Content-Type: application/json" -d '{"url":"https://ravkavonline.co.il"}'``` also does not work, since once again the request body string accepted at the server after decoding is not properly formatted as a JSON object: ```'{url:https://ravkavonline.co.il}'```. 

