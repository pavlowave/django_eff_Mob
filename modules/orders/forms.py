from django import forms
from .models import Order
import json
from typing import Union, Dict, Any, List

class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа.

    Включает поля: номер стола, список блюд в формате JSON, и статус заказа.
    """

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'items': forms.Textarea(attrs={'placeholder': 'Введите блюда в формате JSON или список'}),
        }

    def clean_items(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Очищает данные о блюдах, проверяя их на корректный формат (JSON).

        :return: Данные о блюдах в виде списка или словаря
        :raises forms.ValidationError: если формат данных некорректен
        """
        items_data = self.cleaned_data['items']
        if isinstance(items_data, str):
            try:
                items_data = json.loads(items_data)
            except ValueError:
                raise forms.ValidationError("Некорректный формат данных для блюд.")
        return items_data


class OrderSearchForm(forms.Form):
    """
    Форма для поиска заказов по номеру стола или статусу.
    """

    table_number: forms.IntegerField = forms.IntegerField(
        required=False,
        label='Номер стола',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    status: forms.ChoiceField = forms.ChoiceField(
        choices=[('', 'Все статусы'), ('waiting', 'В ожидании'), ('ready', 'Готово'), ('paid', 'Оплачено')],
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
