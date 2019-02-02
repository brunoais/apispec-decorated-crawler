from brunoais.apispec.ext.decorated_crawler import docd_wraps
from flask import Flask
from marshmallow import Schema, fields
from apispec import APISpec

"""
    This example demonstrates decorated functions that use Marshmallow schemas to serialize their responses.
    The schemas should be included in the resulting schema and refereced from the endpoints.
"""
from flask import Flask

app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title='A safe Random swagger Petstore',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow',
        'brunoais.apispec.ext.decorated_crawler',
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
    pet = {
        "category": [{
            "id": 1,
            "name": "Named"
        }],
        "name": "woof"
    }
    return jsonify(PetSchema().dump(pet).data)

# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

class PetSchema(Schema):
    category = fields.Nested(CategorySchema, many=True)
    name = fields.Str()

spec.definition('Category', schema=CategorySchema)
spec.definition('Pet', schema=PetSchema)

with app.test_request_context():
    spec.add_path(view=random_pet)

if __name__ == "__main__":
    # This should match extended_example_with_marshmallow_output.yaml
    print(spec.to_yaml())

