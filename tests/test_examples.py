import os.path
from importlib import import_module

import pytest
import yaml
from openapi_spec_validator import validate_v2_spec_url

# TODO: Auto-discover the example names
EXAMPLES = [
    "basic_example",
    "extended_example_with_marshmallow",
]


def get_output_file_path(example_name):
    file_path = os.path.join("examples", example_name + "_output.yaml")
    return os.path.abspath(file_path)


@pytest.fixture
def output_file_path(request):
    example_name = request.param
    return get_output_file_path(example_name)


@pytest.fixture
def spec_and_expected_output(request):
    example_name = request.param
    example_module = import_module("examples." + example_name)
    spec = example_module.spec
    output_file_path = get_output_file_path(example_name)
    return spec.to_yaml(), open(output_file_path).read()


@pytest.mark.parametrize('spec_and_expected_output', EXAMPLES, indirect=True)
def test_extended_example_with_marshmallow(spec_and_expected_output):
    spec, expected = spec_and_expected_output

    assert yaml.load(spec) == yaml.load(expected)


@pytest.mark.parametrize('output_file_path', EXAMPLES, indirect=True)
def test_example_outputs_valid_openapiv2(output_file_path):
    validate_v2_spec_url("file://" + output_file_path)
