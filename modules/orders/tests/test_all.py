from modules.orders.models import Order
from django.test import TestCase, Client
from django.urls import reverse


class OrderModelTest(TestCase):

    def setUp(self):
        """
        Создаем тестовые заказы.
        """
        self.order1 = Order.objects.create(
            table_number=5,
            items=[{"name": "Пицца", "price": 10.5}, {"name": "Салат", "price": 5.0}],
            status="waiting"
        )

        self.order2 = Order.objects.create(
            table_number=2,
            items=[{"name": "Паста", "price": 8.0}],
            status="paid",
        )

        self.order3 = Order.objects.create(
            table_number=3,
            items=[{"name": "Бургер", "price": 6.0}, {"name": "Фри", "price": 3.0}],
            status="paid",
        )

    def test_order_total_price_calculation(self):
        """
        Проверяем, что total_price рассчитывается правильно на основе items.
        """
        self.assertEqual(self.order1.total_price, 15.5)
        self.assertEqual(self.order2.total_price, 8.0)
        self.assertEqual(self.order3.total_price, 9.0)

    def test_order_str_representation(self):
        """
        Проверяем строковое представление модели заказа.
        """
        self.assertEqual(str(self.order1), f"Заказ №{self.order1.id} на стол №5 (waiting)")
        self.assertEqual(str(self.order2), f"Заказ №{self.order2.id} на стол №2 (paid)")
        self.assertEqual(str(self.order3), f"Заказ №{self.order3.id} на стол №3 (paid)")

    def test_get_paid_revenue(self):
        """
        Проверяем расчет общей выручки от оплаченных заказов.
        """
        revenue = Order.get_paid_revenue()

        self.assertEqual(revenue, 17)

    def test_order_without_items(self):
        """
        Проверяем создание заказа без указания items (пустой список).
        """
        order = Order.objects.create(table_number=7, status="paid")
        self.assertEqual(order.total_price, 0.0)
        self.assertEqual(order.items, [])

    def test_order_with_single_item(self):
        """
        Проверяем создание заказа с одним элементом в items.
        """
        order = Order.objects.create(
            table_number=8,
            items=[{"name": "Пицца", "price": 12.0}],
            status="paid"
        )
        self.assertEqual(order.total_price, 12.0)


class OrderViewsTest(TestCase):
    def setUp(self):
        """Настройка тестовой базы"""
        self.client = Client()
        self.order = Order.objects.create(table_number=1, items=[{"name": "Суп", "price": 8.0}], status="waiting")

    def test_create_order_view_get(self):
        """Проверяем, что страница создания заказа открывается"""
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')

    def test_delete_order_view(self):
        """Проверяем удаление заказа"""
        response = self.client.post(reverse('delete_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_update_order_status_view(self):
        """Проверяем обновление статуса заказа"""
        response = self.client.post(reverse('update_status', args=[self.order.id]), {'status': 'ready'})
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')

    def test_order_list_view(self):
        """Проверяем, что список заказов отображается корректно"""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Суп")

    def test_calculate_revenue_view(self):
        """Проверяем расчет выручки"""
        Order.objects.create(table_number=2, total_price=3, status="paid")
        Order.objects.create(table_number=3, total_price=30, status="waiting")
        response = self.client.get(reverse('calculate_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3")