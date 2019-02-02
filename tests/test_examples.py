import os.path
from importlib import import_module

import pytest
import yaml
from openapi_spec_validator import validate_v2_spec_url

# TODO: Auto-discover the example names
EXAMPLES = [
    ["extended_example_with_marshmallow"]
]


def get_output_file_path(example_name):
    file_path = os.path.join("examples", example_name + "_output.yaml")
    return os.path.abspath(file_path)


def get_spec_and_expected_output(example_name):
    example_module = import_module("examples." + example_name)
    spec = example_module.spec
    output_file_path = get_output_file_path(example_name)
    return spec.to_yaml(), open(output_file_path).read()


@pytest.mark.parametrize(['example_name'], EXAMPLES)
def test_extended_example_with_marshmallow(example_name):
    spec, expected = get_spec_and_expected_output(example_name)

    assert yaml.load(spec) == yaml.load(expected)


@pytest.mark.parametrize(['example_name'], EXAMPLES)
def test_example_outputs_valid_openapiv2(example_name):
    output_file_path = get_output_file_path(example_name)
    validate_v2_spec_url("file://" + output_file_path)
