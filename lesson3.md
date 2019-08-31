#### Use case 1
We are looking for a new shirt. We ask the slaesperson to show us the different shirts we have.
HINT:
Shirts will be of the format {"shirtID": 123, "color": "blue", "price": 35}.
We will return a list of shirts.

Request:

```

```

Response:
```

```

#### Use case 2
We liked on of the shirts and we ask the salesperson for that shirt in our size.
HINT:
We can say we want a particular shirt by giving the shirtID and the size as arguments
A particular sized shirt will be of the format {"shirtID": 123, "color": "blue", "size": 36, "price":35}
We return the correct size shirt in response

Request
```

```

Response
```

```

#### Use case 3
The salesperson brought the shirt that you wanted, but you don't want to buy it anymore. You tell them that you want to cancel your request to buy the shirt. You send the shirtID in the request.

Request
```

```

Response

```

```

#### Use case 4
We want to buy a shirt. We pass shirtID as argument and also give money in the format:
{
  10 Euros : 2 notes,
  5 Euros: 1 note,
  1 Euro: 3 notes,
}
NOTE: This is some data that we want to give the server

Request:
```

```

We get the shirt that we paid for in the response.
Response:
```

```

What will be the response if the money is not same as the price of the shirt?
HINT: We should give a bad response
Response:
```

```

#### Use case 5
You bought the shirt, but it is not of the correct size. You want to exchange the shirt and get the one with the correct size. This is similar to a fix/update. You give the shirt in the request, you get another shirt in response.

Request:
```

```

Response:
```

```
