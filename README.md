# Bucket List API
[![Build Status](https://travis-ci.org/jokamjohn/bucket_api.svg?branch=master)](https://travis-ci.org/jokamjohn/bucket_api)
[![Coverage Status](https://coveralls.io/repos/github/jokamjohn/bucket_api/badge.svg)](https://coveralls.io/github/jokamjohn/bucket_api)
[![BCH compliance](https://bettercodehub.com/edge/badge/jokamjohn/bucket_api?branch=master)](https://bettercodehub.com/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cfda51ef2f8946639eb34b11fa8b5480)](https://www.codacy.com/app/jokamjohn/bucket_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jokamjohn/bucket_api&amp;utm_campaign=Badge_Grade)

The api enables you to create/ register a user within the application.

## Usage

### User registration.
Send a `POST` request to `auth/register` endpoint with the payload in
`Json`

An example would be
```
{
  "email": "example@gmail.com",
  "password": "123456"
}
```

The email value must be a valid email format and the password must be
four characters and above.
If the email is invalid or empty and the password is empty or less than
four character, the response `status` will be `failed` with the `message`
`Missing or wrong email format or password is less than four characters`
and a `status code` of `202`

As shown below:
```
{
    "message": "Missing or wrong email format or password",
    "status": "failed"
}
```

If the user already exists then they wont be registered again, the
following response will be returned.
```
{
    "message": "Failed, User already exists, Please sign In",
    "status": "failed"
}
```

If the request is successful and the user has been registered the
response below is returned. With an auth token
```
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM0ODQ5OTYsImlhdCI6MTUwMzM5ODU4Niwic3ViIjo1fQ.GC6IEOohdo_xrz9__UeugIlir0qtJdKbEzBtLgqjt5A",
    "message": "Successfully registered",
    "status": "success"
}
```

### User Login
The user is able to login by send sending a `POST` request to
`auth/login` with the json payload below.
```
{
  "email": "example@gmail.com",
  "password": "123456"
}
```

If the request is successful the following response is returned:
```
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM0OTIzMzQsImlhdCI6MTUwMzQwNTkyNCwic3ViIjo1fQ.dRDTIP93WNRNv5Q7vCLLHuZfwvH5ze2B_VdRm6qHJbU",
    "message": "Successfully logged In",
    "status": "success"
}
```

Otherwise if the email is invalid, user with the email does not exist or
the password length is incorrect or less than four characters, the
following response is returned.
```
{
    "message": "Missing or wrong email format or password is less than four characters",
    "status": "failed"
}
```

### User Logout
The api also enables a user to logout. The `auth/logout` endpoint
provides this functionality.
The `POST` request to the endpoint must have an `Authorization`
header containing the auth token, otherwise the user wont be logged out.

Example of the Authorization header
```
Authorization Bearer <token>
```

If the operation is successful, the response below will be returned.
```
{
    "message": "Successfully logged out",
    "status": "success"
}
```

If the token has expired this will be returned.

```
{
    "message": "Signature expired, Please sign in again",
    "status": "failed"
}
```

For an invalid token
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}

```

Without an Authorization header
```
{
    "message": "Provide an authorization header",
    "status": "failed"
}
```

## BucketList
The user is also able to create and get back a list of their buckets.
### Create Bucket
Below is an example of a request to create a bucket. **name** is a
required attribute. An auth token must be attached in the Authorization
header
```
{
  "name": "Travel"
}
```
The following response will be returned
```
{
    "createdAt": "Wed, 23 Aug 2017 10:14:52 GMT",
    "id": 2,
    "modifiedAt": "Wed, 23 Aug 2017 10:14:52 GMT",
    "name": "Travel",
    "status": "success"
}
```
### Get user`s Buckets
Below is an example of a *get* request endpoint to get the users buckets.
An auth token must be attached in the Authorization
header
```
/bucketlists
```

## Running tests
Before running the application tests, update your env variables
```
export  APP_SETTINGS=app.config.TestingConfig
export DATABASE_URL_TEST=<postgres database url>
```
### Running tests without coverage
You can now run the tests from the terminal
```
python manage.py test
```
### Running tests with coverage
You can also run tests with coverage
```
python manage.py cov
```
After the tests have run the coverage report will be opened in your
default browser where you can see the results.