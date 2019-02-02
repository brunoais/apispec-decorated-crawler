# apispec-decorated-crawler

Plugin for apispec which helps reusing the documentation by using a decorated function stack.

## Basic Example
 
With this setup:

```python
from flask import Flask
from apispec.ext.decorated_crawler import docd_wraps

app = Flask(__name__)


def decorates(func):
@docd_wraps(func)
def calling(*args, **kwargs):
    '''
    ---
    get:
	consumes:
	  - application/xml+dec1
	security:
	    - AlmostBasicAuth: []
	      BasicAuth: []
	    - ApiKeyAuth: []
	tags:
	    - down1
	    - up1
	responses:
	    400:
		description: he may fail {f[x-400-suffix]}
		schema: PetSchema
    _:
	responses:
	    400:
		description: Global fail
		schema: PetSchema
    '''
    return func(*args, **kwargs)

return calling

def decorates2(func):
@docd_wraps(func)
def calling(*args, **kwargs):
    '''
    ---
    get:
	tags:
	    - get2
	    - up1
	security:
	    - OAuth2: [scope1, scope2]
	responses:
	    402:
		description: mefail
		schema: PetSchema
    '''
    return func(*args, **kwargs)

return calling
```

Passing a view function:

```python
@app.route('/random/<kind>')
@decorates
@decorates2
def random_pet(kind):
    '''A cute furry animal endpoint.
    ---

    post:
        description: POST a pet
    get:
        description: Get a pet
        security:
            - ApiKeyAuth: []
        consumes:
          - application/json
          - application/xml
        produces:
          - application/json
          - application/xml
        parameters:
            - in: path
              name: kind
              required: true
              type: string
              description: Path Parameter description in Markdown.
            - in: query
              name: offset
              type: string
              description: Query Parameter description in Markdown.
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
            400:
                x-400-suffix: yeah yeah....
    '''
    pet = {
        "category": [{
            "id": 1,
            "name": "Named"
        }],
        "name": "woof"
    }
    return jsonify(PetSchema().dump(pet).data)


with app.test_request_context():
    spec.add_path(view=gist_detail)
```

Passing a method view function::

```python
from flask.views import MethodView

class PetApi(MethodView):
@decorates
@decorates2
def get(kind):
    '''A cute furry animal endpoint.
    ---
    description: Get a pet
    security:
	- ApiKeyAuth: []
    consumes:
      - application/json
      - application/xml
    produces:
      - application/json
      - application/xml
    parameters:
	- in: path
	  name: kind
	  required: true
	  type: string
	  description: Path Parameter description in Markdown.
	- in: query
	  name: offset
	  type: string
	  description: Query Parameter description in Markdown.
    responses:
	200:
	    description: A pet to be returned
	    schema: PetSchema
	400:
	    x-400-suffix: yeah yeah....
    '''
    pet = {
	"category": [{
	    "id": 1,
	    "name": "Named"
	}],
	"name": "woof"
    }
    return jsonify(PetSchema().dump(pet).data)


def post(self):
    '''A cute furry animal endpoint.
    ---

	description: POST a pet
    '''
   pass

method_view = PetApi.as_view('randomPet')
app.add_url_rule("/random/<kind>", view_func=method_view)
with app.test_request_context():
    spec.add_path(view=method_view)
```

The result will be:

```python
print(spec.to_dict()['paths'])
# OrderedDict([
    ('/random',
    OrderedDict([
        ('post',
          {'description': 'POST a pet',
          'responses': {400: {'description': 'Global fail', 'schema': {'$ref': '#/definitions/Pet'}}}}),
        ('get',
        {'description': 'Get a pet',
        'security': [{'ApiKeyAuth': []}, {'AlmostBasicAuth': [], 'BasicAuth': []}, {'OAuth2': ['scope1', 'scope2']}],
        'consumes': ['application/json', 'application/xml', 'application/xml+dec1'],
        'produces': ['application/json', 'application/xml'],
        'parameters': [{'in': 'path', 'name': 'kind', 'required': True, 'type': 'string', 'description': 'Path Parameter description in Markdown.'}, {'in': 'query', 'name': 'offset', 'type': 'string', 'description': 'Query Parameter description in Markdown.'}],
        'responses': {200: {'description': 'A pet to be returned', 'schema': {'$ref': '#/definitions/Pet'}},
        400: {'x-400-suffix': 'yeah yeah....', 'description': 'he may fail yeah yeah....'},
        402: {'description': 'mefail', 'schema': {'$ref': '#/definitions/Pet'}}}, 'tags': ['down1', 'up1', 'get2']})]))])
```

## More examples

For more examples, please see the scripts in the examples subdirectory.

## Details

This is an operations helper that allows you to pass a decorated view and get the combined documentation of all decorator functions.
It required the view passed to `add_path`. Inspects view docstrings and its docd_wraps decorator functions and merges all the
documentation into a single document.
Useful if you use decorators to manage authentication or even if you have shared error pages and you do not
want to document common error states (status 400, status 500, etc...) individually on all views.

All documentation is merged from bottom-up, starting on the view function and ending on the topmost decorator.
Decorators can declare a "special" HTTP method called _ (underscore). That one is applied last for all methods,
also from bottom up, in a subsequent pass.


## Installation

    pip install apispec-decorated-crawler

## License

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
