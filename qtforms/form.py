import typing
from qtpy import QtWidgets, QtCore
from pydantic import BaseModel, ValidationError
from typing import Type, Optional, Dict
from .protocols import WidgetRegistry
from .wrappers import FieldError


class Form(QtWidgets.QWidget):
    submit = QtCore.Signal(BaseModel)
    error = QtCore.Signal(ValidationError)
    keys_changed = QtCore.Signal(set)

    def __init__(
        self,
        widget_registry: WidgetRegistry,
        model_class: Type[BaseModel],
        initial_data: Optional[Dict[str, typing.Any]] = None,
        initial_validation: bool = True,
        auto_submit: bool = False,
        auto_validate: bool = True,
        set_field_errors: bool = True,
        submit_button:  QtWidgets.QWidget | None = None,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        """
        A Validated Form

        This form uses the pydantic model to validate the data and
        emit signals when the data is valid or invalid. It uses the
        widget registry to spawn widgets for the fields. Data is validated
        when the user changes the value of a field, and two-way data binding
        is established between the model and the widget.

        Parameters
        ----------
        widget_registry : WidgetRegistry
            The widget registry to use to spawn widgets for the fields
        model_class : Type[BaseModel]
            The model class to use to validate the data. 
            This class must be a pydantic model class. 
            Not an instance of a model class.
        initial_data : Optional[Dict[str, typing.Any]], optional
            Initial data for the form., by default None
        auto_submit : bool, optional
            Should we auto submit on change of data (will not render a submit button),
              by default False
        auto_validate : bool, optional
            Should we auto validate on change of data (will not render a submit button),
              by default False
        set_field_errors : bool, optional
            Should the field errors appear next to the field?, by default True
        initial_validation : bool, optional
            Should we validate the initial data?, by default True
        submit_button :  QtWidgets.QWidget | None, optional
            The submit button to use, a default one will be created if None and auto_submit is False, by default None
        parent : QtWidgets.QWidget | None, optional
            The parent for this widget, by default None
        """
        super().__init__(parent)
        self.widget_registry = widget_registry

        self.model = None
        self.initial_data = initial_data or {}

        self.modelclass = model_class 

        self.widgets = {}
        self.auto_submit = auto_submit

        self.set_field_errors = set_field_errors

        self.auto_validate = auto_validate

        self.unvalidated_values = self.initial_data.copy()

        if not self.auto_submit:
            self.submit_button = submit_button or QtWidgets.QPushButton("Submit")
        else:
            self.submit_button = None


        self.setup_widgets()

        self.setup_ui()

        if initial_validation:
            self.validate(self)


    def setup_widgets(self):
        """
        Set up the widgets for each field in the model class.
        """
        for i in self.modelclass.__fields__.values():
            self.widgets[i.name] = self.widget_registry.get_widget_for_field(i, self)
            self.widgets[i.name].connect_signals(self)

        self._connect_signals()
        

    def check_changed_keys(
        self, previous_data: Dict[str, typing.Any], model: BaseModel
    ) -> set:
        """
        Checks if the model has changed since the last time it was validated.

        Parameters
        ----------
        previous_data : Dict[str, typing.Any]
            The previous data used for validation.
        model : BaseModel
            The model to compare with.

        Returns
        -------
        set
            A set of keys that have changed.
        """
        keys = set()
        for field in model.__fields__.values():
            if field.name not in previous_data:
                keys.add(field.name)
                continue

            if previous_data[field.name] != getattr(model, field.name):
                keys.add(field.name)

        return keys

    def validate(self, is_submit_validation=False):
        """
        Validate the form data using the model class.

        Parameters
        ----------
        is_submit_validation : bool, optional
            Indicates if the validation is triggered by a submit action, by default False
        """
        try:
            self.model = self.modelclass(**self.unvalidated_values)
            changed_keys = self.check_changed_keys(self.unvalidated_values, self.model)
            if changed_keys:
                self.keys_changed.emit(changed_keys)

            for field in self.model.__fields__.values():
                # Establish model -> widget binding
                print(field.name)
                self.widgets[field.name].set_error(None)
                self.widgets[field.name].set_value(getattr(self.model, field.name))

            if self.submit_button:
                self.submit_button.setEnabled(True)

            if is_submit_validation or self.auto_submit:
                self.submit.emit(self.model)

        except ValidationError as e:
            if self.submit_button:
                self.submit_button.setEnabled(False)

            if self.set_field_errors:
                # Sets the field errors
                for field_error in e.errors():
                    first_field = field_error["loc"][0]
                    if first_field in self.widgets:
                        self.widgets[first_field].set_error(FieldError(**field_error))

            if is_submit_validation or self.auto_submit:
                self.error.emit(e)

    def submit_pressed(self):
        """
        Triggered when the submit button is pressed.
        """
        self.validate(is_submit_validation=True)

    def setup_ui(self):
        """
        Set up the user interface by adding widgets to the layout.
        """
        self.formLayout = QtWidgets.QVBoxLayout()

        for widget in self.widgets.values():
            self.formLayout.addWidget(widget)

        self.setLayout(self.formLayout)

        if self.submit_button:
            self.formLayout.addWidget(self.submit_button)

    def _connect_signals(self):
        """
        Connect the signals between the widgets and the model class.
        """
        for key, value in self.modelclass.__fields__.items():
            # Establish widget -> model binding
            self.widgets[key].connect_signals(self)

        if self.submit_button:
            self.submit_button.clicked.connect(self.submit_pressed)

    def on_property_changed(self, property_name: str, value: typing.Any) -> None:
        """
        Triggered when a property of a widget is changed.

        Parameters
        ----------
        property_name : str
            The name of the property that changed.
        value : typing.Any
            The new value of the property.
        """
        self.unvalidated_values[property_name] = value
        print(property_name, value)
        print(self.unvalidated_values)
        if self.auto_validate:
            self.validate(self.unvalidated_values)

    def reset(self):
        """
        Reset the form to its initial state.
        """
        self.validate(self.initial_data)