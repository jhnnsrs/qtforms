import typing
from qtpy import QtWidgets
from typing import Protocol, Optional, TYPE_CHECKING
from .wrappers import FieldError
from pydantic import Field


if TYPE_CHECKING:
    from .form import Form


class FormWidget(QtWidgets.QWidget):
    def set_value(self, value: Optional[typing.Any]):
        ...

    def set_error(self, error: Optional[FieldError]):
        ...

    def connect_signals(self, controller: "Form"):
        ...



class WidgetRegistry(Protocol):
    def get_widget_for_field(
        self, field: Field, parent: QtWidgets.QWidget | None = None
    ) -> QtWidgets.QWidget:
        """Return a widget for the given field"""
        ...

