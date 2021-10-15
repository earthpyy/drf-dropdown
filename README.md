# django-rest-dropdown

![GitHub](https://img.shields.io/github/license/earthpyy/django-rest-dropdown)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/earthpyy/django-rest-dropdown/CI)
![PyPI](https://img.shields.io/pypi/v/django-rest-dropdown)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-rest-dropdown)
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
