# drf-dropdown

![GitHub](https://img.shields.io/github/license/earthpyy/drf-dropdown)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/earthpyy/drf-dropdown/CI)
![PyPI](https://img.shields.io/pypi/v/drf-dropdown)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/drf-dropdown)
![Django Version](https://img.shields.io/badge/django-3.0%20%7C%203.1%20%7C%203.2-blue)
![Django REST Version](https://img.shields.io/badge/djangorestframework-3.11%20%7C%203.12-blue)
![Pre-commit Enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

Dropdown population implementation for Django REST Framework

## Usage

### Add `DropdownView` to API URL

```python
# urls.py
import dropdown

urlpatterns = [
    ...
    path('dropdown/', dropdown.DropdownView.as_view(), name='dropdown'),
]
```

### Define new dropdown

```python
# someapp/dropdown.py
import dropdown

@dropdown.register
def users(query='', **kwargs):
    return dropdown.from_model(User, label_field='email')
```

## Development

### Set Up

```bash
make setup
```
