from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from marshmallow import Schema, fields

from brunoais.apispec.ext.decorated_crawler import DecoratedCrawler, docd_wraps

"""
    This example demonstrates decorated functions that use Marshmallow schemas to serialize their responses.
    The schemas should be included in the resulting schema and referenced from the endpoints.
"""
app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title='A safe Random swagger Petstore',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        # Note that Decorated crawler has to be placed before MarshmallowPlugin for resolution
        # of schema references in decorator comments to work
        DecoratedCrawler(),
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


def decorates(func):
    @docd_wraps(func)
    def calling(*args, **kwargs):
        """
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
        """
        return func(*args, **kwargs)

    return calling


def decorates2(func):
    @docd_wraps(func)
    def calling(*args, **kwargs):
        """
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
        """

        return func(*args, **kwargs)

    return calling


@app.route('/random/<kind>')
@decorates
@decorates2
def random_pet(kind):
    """

    A cute furry animal endpoint.
    ---

    post:
        description: POST a pet
        parameters:
            - in: path
              name: kind
              required: true
              type: string
              description: Path Parameter description in Markdown.
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
    """
    pass


# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class PetSchema(Schema):
    category = fields.Nested(CategorySchema, many=True)
    name = fields.Str()


spec.components.schema('Category', schema=CategorySchema)
spec.components.schema('Pet', schema=PetSchema)

with app.test_request_context():
    spec.path(view=random_pet)


if __name__ == "__main__":
    # This should match extended_example_with_marshmallow_output.yaml
    print(spec.to_yaml())
