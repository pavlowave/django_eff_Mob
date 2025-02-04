from django.db import models
from django.db.models import Sum
from typing import List, Dict, Union, Tuple, Any, Optional

class Order(models.Model):
    """
    Модель, представляющая заказ с полями для номера стола, списка блюд,
    общей стоимости и статуса.
    """

    STATUS_CHOICES: List[Tuple[str, str]] = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: int = models.IntegerField()
    items: Union[List[Dict[str, Union[str, float]]], Dict[str, Union[str, float]]] = models.JSONField(default=list, blank=True)
    total_price: float = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def save(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Переопределенный метод сохранения заказа. Рассчитывает общую стоимость
        заказа перед его сохранением.

        Если items является списком, метод суммирует цены всех элементов
        перед сохранением объекта в базу данных.

        :param args: Дополнительные позиционные аргументы
        :param kwargs: Дополнительные именованные аргументы
        :return: None
        """
        if isinstance(self.items, list):
            self.total_price = sum(item.get('price', 0) for item in self.items)

        super().save(*args, **kwargs)

    @classmethod
    def get_paid_revenue(cls) -> float:
        """
        Рассчитывает общую выручку от оплаченных заказов.

        Метод фильтрует заказы со статусом 'paid' и суммирует их total_price.

        :param cls: Класс модели (Order)
        :return: Общая сумма выручки от всех оплаченных заказов
        """
        total: Optional[float] = cls.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum']
        return total or 0.0

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа.

        :return: Читаемое строковое описание заказа
        """
        return f"Заказ №{self.id} на стол №{self.table_number} ({self.status})"
