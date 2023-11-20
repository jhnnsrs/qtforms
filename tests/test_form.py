import pytest
from qtforms.form import Form


from qtforms.labeled_registry import LabeledWidgetRegistry
from pydantic import BaseModel, validator, Field



class MyModel(BaseModel):
    name: str = Field("hundi", min_length=3, max_length=50, description="Your name")
    number: int = Field(1, ge=0, le=100, description="A number between 0 and 100")

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("Name must have a space")
        return v.title()



@pytest.fixture
def form_instance(qtbot):
    widget_registry = LabeledWidgetRegistry()
    return Form(widget_registry, MyModel)

def test_init(form_instance):
    assert form_instance.widget_registry is not None
    assert form_instance.modelclass is not None

def test_setup_widgets(form_instance):
    form_instance.setup_widgets()
    assert form_instance.widgets is not None

def test_check_changed_keys(form_instance):
    previous_data = {"name": "hundi", "number": 1}
    model = MyModel(name="ggg  hh", number=1)
    assert form_instance.check_changed_keys(previous_data, model).pop() == "name"

def test_validate(form_instance):
    form_instance.validate()

def test_submit_pressed(form_instance):
    form_instance.submit_pressed()

def test_setup_ui(form_instance):
    form_instance.setup_ui()

def test_connect_signals(form_instance):
    form_instance._connect_signals()

def test_on_property_changed(form_instance):
    form_instance.on_property_changed("property_name", "value")

def test_reset(form_instance):
    form_instance.reset()