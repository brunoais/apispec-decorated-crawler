from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask.views import MethodView

from brunoais.apispec.ext.decorated_crawler import DecoratedCrawler, docd_wraps

"""
    This example demonstrates some spec merging using decorators for normal and
    MethodView endpoints.
"""
app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title='A safe Random swagger Petstore',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        DecoratedCrawler(),
        FlaskPlugin(),
    ],
)


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
                    description: he may fail
                    schema:
                      type: string
        _:
            responses:
                400:
                    description: Global fail
                    schema:
                      type: string
                      example: something global went wrong
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
                    schema:
                      type: string
                      example: decorate2 error
        '''
        return func(*args, **kwargs)

    return calling


@app.route('/random/<kind>')
@decorates
@decorates2
def random_pet(kind):
    '''A cute furry animal endpoint.
    ---

    post:
        description: POST a pet
        parameters:
            - in: path
              name: kind
              required: true
              type: string
              description: Path Parameter description in Markdown.
        responses:
            200:
                description: Pet POSTed successfully
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
                schema:
                  type: string
                  example: fido
            400:
                description: Something went wrong
    '''
    pass


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
                schema:
                  type: string
                  example: fido
        '''
        pass

    def post(self):
        '''A cute furry animal endpoint.
        ---
        description: POST a pet
        parameters:
            - in: path
              name: kind
              required: true
              type: string
              description: Path Parameter description in Markdown.
        responses:
            200:
                description: Pet POSTed successfully
        '''
        pass


method_view = PetApi.as_view('randomPet')
app.add_url_rule("/random2/<kind>", view_func=method_view)
with app.test_request_context():
    spec.path(view=random_pet)
    spec.path(view=method_view)

if __name__ == "__main__":
    # This should match basic_example.yaml
    print(spec.to_yaml())
