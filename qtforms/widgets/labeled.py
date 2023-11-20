import typing
from qtpy import QtWidgets
from pydantic import Field, ValidationError
from typing import Optional
from functools import partial
from enum import Enum
from qtforms.wrappers import FieldError
from qtforms.form import Form

class BaseLabeledWidget(QtWidgets.QWidget):
    """A base class for all labeled widgets.

    This class includes the logic for setting the error, label, and description
    if they are present.

    Attributes:
        field (Field): The field associated with the widget.
        error_widget (QtWidgets.QLabel): The widget used to display error messages.
        label_widget (QtWidgets.QLabel): The widget used to display the label.
        description_widget (Optional[QtWidgets.QLabel]): The widget used to display the description,
            or None if no description is provided.
    """

    def __init__(self, field: Field, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.field = field

        self.error_widget = QtWidgets.QLabel()
        self.error_widget.hide()

        self.label_widget = QtWidgets.QLabel(self.field.name)

        if self.field.field_info.description:
            self.description_widget = QtWidgets.QLabel(
                self.field.field_info.description
            )
        else:
            self.description_widget = None

        self.setup_ui(self.error_widget, self.label_widget, self.description_widget)

    def setup_ui(
        self,
        error: QtWidgets.QLabel,
        label: QtWidgets.QLabel,
        description: Optional[QtWidgets.QLabel],
    ):
        raise NotImplementedError("Must be implemented by subclass")

    def set_error(self, error: Optional[FieldError]):
        """Set the error message and display it if an error is provided.

        Args:
            error (Optional[FieldError]): The error object containing the error message,
                or None if there is no error.
        """
        if error is None:
            self.error_widget.setText("")
            self.error_widget.hide()
        else:
            self.error_widget.setText(error.msg)
            self.error_widget.show()


class LabeledLineWidget(BaseLabeledWidget):
    def setup_ui(
        self,
        error: QtWidgets.QLabel,
        label: QtWidgets.QLabel,
        description: Optional[QtWidgets.QLabel],
    ):
        self.real_widget = QtWidgets.QLineEdit()

        formLayout = QtWidgets.QVBoxLayout()

        formLayout.addWidget(label)
        formLayout.addWidget(self.real_widget)
        formLayout.addWidget(description)
        formLayout.addWidget(error)
        self.setLayout(formLayout)

    def connect_signals(self, controller: "Form"):
        self.real_widget.textChanged.connect(
            partial(controller.on_property_changed, self.field.name)
        )

    def set_value(self, value: Optional[typing.Any]):
        if value is None:
            value = ""

        if value != self.real_widget.text():
            self.real_widget.setText(value)


class LabeledIntWidget(BaseLabeledWidget):
    def setup_ui(
        self,
        error: QtWidgets.QLabel,
        label: QtWidgets.QLabel,
        description: Optional[QtWidgets.QLabel],
    ):
        self.real_widget = QtWidgets.QLineEdit()

        formLayout = QtWidgets.QVBoxLayout()

        formLayout.addWidget(label)
        formLayout.addWidget(self.real_widget)
        formLayout.addWidget(description)
        formLayout.addWidget(error)
        self.setLayout(formLayout)

    def connect_signals(self, controller: "Form"):
        self.real_widget.textChanged.connect(
            partial(controller.on_property_changed, self.field.name)
        )

    def set_value(self, value: Optional[typing.Any]):
        if value is None:
            value = ""

        value = str(value) # convert to string
        if value != self.real_widget.text():
            self.real_widget.setText(value)
