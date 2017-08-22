# Bucket List API
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