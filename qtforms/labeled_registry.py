from qtpy import QtWidgets
from pydantic import Field
from .widgets.labeled import LabeledIntWidget, LabeledLineWidget


class LabeledWidgetRegistry:
    """ A registry for widgets that are labeled and have a description and error+label
    
    This class provides a registry for widgets that are labeled and have a description and error+label.
    It allows for easy retrieval of labeled widgets based on the field type.
    
    Attributes:
        with_description (bool): Indicates whether the widgets should have a description.
        with_label (bool): Indicates whether the widgets should have a label.
        with_errors (bool): Indicates whether the widgets should have an error label.
    """


    def __init__(
        self,
        with_description: bool = True,
        with_label: bool = True,
        with_errors: bool = True,
    ) -> None:
        self.with_description = with_description
        self.with_label = with_label
        self.with_errors = with_errors

    def get_widget_for_field(self, field: Field, parent: QtWidgets.QWidget | None = None):
        """Returns a labeled widget for the given field
        
        Args:
            field (Field): The field for which to retrieve the labeled widget.
            parent (QtWidgets.QWidget | None): The parent widget for the labeled widget.
        
        Returns:
            QtWidgets.QWidget: The labeled widget for the given field.
        
        Raises:
            NotImplementedError: If no widget is available for the given field type.
        """
        try:
            # subclass test
            if issubclass(field.type_, str):
                return LabeledLineWidget(field, parent)

            elif issubclass(field.type_, int):
                return LabeledIntWidget(field, parent)

            else:
                raise NotImplementedError(
                    f"No widget for this field {field} of type {field.type_}"
                )

        except TypeError as e:
            raise NotImplementedError(f"No widget for this field {field}") from e
