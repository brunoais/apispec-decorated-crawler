# apispec-decorated-crawler

Plugin for apispec which helps reusing the documentation by using a decorated function stack.

## Examples

For basic and extended examples, please see the scripts in the examples subdirectory.

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
