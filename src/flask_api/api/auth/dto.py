"""Parsers and serializers for /auth API endpoints."""
from flask_restx import Model
from flask_restx.fields import String, Boolean
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser


# Bundle: Report all error instead of the first.
auth_reqparser = RequestParser(bundle_errors=True)
auth_reqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
auth_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)
"""
"User" is the name of the API Model, and this value will be used to identify
the JSON object in the Swagger UI page. Please read the Flask-RESTx documentation
for detailed examples of creating API models. Basically, an API model is a
dictionary where the keys are the names of attributes on the object that
we need to serialize, and the values are a class from the fields module
that formats the value of the attibute on the object to ensure that
it can be safely included in the HTTP response.

Any other attributes of the object are considered private and will not be
included in the JSON. If the name of the attribute on the object is different
than the name that you wish to use in the JSON, specify the name of the attribute
on the object using the attribute parameter, which is what we are doing
for registered_on in the code above.
"""
user_model = Model(
    "User",
    {
        "email": String,
        "public_id": String,
        "admin": Boolean,
        "registered_on": String(attribute="registered_on_str"),
        "token_expires_in": String,
    },
)
