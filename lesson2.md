## Basics of HTTP

#### Request format
```
GET /users/ HTTP1.1
Header1 : ...
Header2 : ...
Header3 : ...
...

Body of the request: ....
```

#### Response format
```
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 24204

HTML
<html> .... </html>

JSON
{
 ...
}

File -> bytes 0101010101010
```

When you do a download, it shows the size of the download before the whole file downloads. This is because of the Content-lenght header


### RESTUARANT EXAMPLE FOR AN API

#### Use case 1
We ask the waiter to get the menu so that we can order.

Request:

```
GET /menu/ HTTP1.1
Host: www.waiter.com
```
Response:
```
HTTP1.1 OK 200
Content-type: text/json

{
  menu = [
    {
      item1: fish,
      price: 20
    },
    {
      item2: chicken,
      price: 20
    },
    {
      item3: pasta,
      price: 10
    }
  ]
}
```
#### Use case 2
Whenever we want to give some information with GET request, we pass as URL parameters
Format for URL parameters: ?param1=value1&param2=value2

Request
```
GET /order?item=1&item=2 HTTP1.1
Host: www.waiter.com


```
Response
```
HTTP1.1 200 OK
Content-type: Food

{
  item: item1,
  item: item2
}
```

#### Use case 3
Another way for ordering something from the menu is by pointing to something in the menu
This will also inform the waiter what you want to order, but it is not the correct way of ordering
This is considered a bad request

Request
```
GET /order HTTP1.1
Host: www.waiter.com

{
  item=1,
  item=2
}
```
#### Use case 4
When you have ordered something and you want to cancel the order becauseof some reason
You make a request to the waiter to ask the kitchen to cancel your order
The kitchen may cancel your order if it is not ready and the waiter will give you confirmation

Request
```
DELETE /order?item=1&item=2 HTTP1.1
Host: www.waiter.com

```

Response

```
HTTP1.1 200 OK
Content-type: message

Yes order cancelled
```

The kitchen may not cancel the order if it has already been prepared
This is a bad response.

Response
```
HTTP1.1 403 Forbidden
Content-type: message

The order has been prepared already, so we can't cancel.
```
#### Use case 5
When you want to pay for your order, you will give the waiter money.
The money is some information that you want to give the server
This information has to be passed in the request body

Request:
```
POST/PUT /pay/ HTTP1.1
Host: waiter

{
  10 Euros : 2 notes,
  5 Euros: 1 note,
  1 Euro: 3 notes,
}
```

You may not get any response for POST/PUT/PATCH, etc but it is always good to get a response.
Response:
```
HTTP1.1 200 OK
Content-type: message

Thanks for paying.
```
#### Use case 6
PATCH request is mostly used to fix/change/update something that is already in the server
You want no garlic in your chicken, you ask the waiter to fix the item, you give the item to the waiter.
Waiter will go to the kitchen and ask them to fix and he will give you a confirmation message.

Request:
```
PATCH /nogarlic/ HTTP1.1
Host: waiter

{
  item: chicken,
}
```

Response:
```
HTTP1.1 200 OK
Content-type: message

Given to the kitchen to fix.
```

#### Use case 7
If you're using HTTP you will have to make another request to get the item.
Once the waiter has given a response, you will have to make another request to get your food.
So we make another GET request for the waiter to bring the fixed item.

Request:
```
GET /fixeditem/ HTTP1.1
Host: waiter

```

Response:
```
HTTP1.1 200 OK
Content-type: food

{
  item: chicken,
}
```

#### Use case 8
In some cases, waiter will not give you any confirmation.
He will take your item to the kitchen and will only come back to you after your item has been fixed.
When he comes back he brings the new/fixed item.

Request:
```
PATCH /nogarlic/ HTTP1.1
Host: waiter

{
  item: chicken,
}
```

Response:
```
HTTP1.1 200 OK
Content-type: food

{
  item: chicken,
}
```

### WHAT DOES FLASK DO?
- What are my Use cases?
- What will be the request and the response for each use case?
- Then start programming


**Each function in flask is a use case**
Similar use cases can be grouped in a single function
example:
Use case 1: Get ***information about a user*** in an application
Use case 2: Update the ***information about a user*** in an application

Here you make a single function to get and update the information of the user,
This is where HTTP requests play a part.
You can say that Use case 1 will be a GET request and Use case 2 will be a PATCH request

```
@app.route("/user", methods=["GET", "PATCH"])
def user():
  if request.method == "GET":
    // Get the information of the user and return in the response
  if request.method == "PATCH":
    // You need to get the new information from the request body
    // Update this information on the server
    // Give a response with the new information
```


You can make a giant function, that will handle all your use cases
```
  if request.line == /user then you give the user information
  if request.line == /register you register
  if request.line == /login you login
```
