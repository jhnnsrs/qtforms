# mikro

[![codecov](https://codecov.io/gh/jhnnsrs/qtforms/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/qtforms)
[![PyPI version](https://badge.fury.io/py/qtforms.svg)](https://pypi.org/project/qtforms/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/qtforms/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/qtforms.svg)](https://pypi.python.org/pypi/qtforms/)
[![PyPI status](https://img.shields.io/pypi/status/qtforms.svg)](https://pypi.python.org/pypi/qtforms/)
[![PyPI download month](https://img.shields.io/pypi/dm/qtforms.svg)](https://pypi.python.org/pypi/qtforms/)

qtforms is a library that allows you to create simple forms in Qt for Python with the help of
pydantic.



### Installation

```bash
pip install qtforms
```


# Quick Start

```python
from qtpy import QtWidgets
from pydantic import BaseModel, validator, Field
import sys

from qtforms.labeled_registry import LabeledWidgetRegistry
from qtforms.form import Form


class MyModel(BaseModel):
    name: str = Field("hundi", min_length=3, max_length=50, description="Your name")
    number: int = Field(1, ge=0, le=100, description="A number between 0 and 100")

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("Name must have a space")
        return v.title()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    model = MyModel(name="hello world")
    ##model.events.name.connect(lambda x: print(x))

    form = Form(LabeledWidgetRegistry(), MyModel, initial_data=dict(name="hello world"), auto_validate=True)
    form.submit.connect(lambda x: print(x))

    form.show()
    sys.exit(app.exec_())

```


### Design

For the design of qtform, we use the following design:

`Form` is the container and controller for the form. It calls the widget registry to spawn the widgets for the fields.
These widgets need to follow the `FormWidget` interface, and implement functions to set values and report errors.

`Form` also handles the validation of the form, and emits a `submit` signal when the form is valid and the submit button is pressed
(or when auto_submit is enabled on each valid change). Validation is done by pydantic, and the validated values are immediately
reported to the widgets.


