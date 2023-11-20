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
