from django.urls import resolve
from django.test import TestCase
from .views import home_page
from .models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEquals(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item', 'option_text': 'Alta'})

        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item', 'option_text': 'Alta'})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'], '/lists/the-only-list-in-the-world/')

    def test_displays_all_list_itens(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())



class ItemModelTest(TestCase):

    def test_saving_and_retriving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEquals(first_saved_item.text, 'The first (ever) list item')
        self.assertEquals(second_saved_item.text, 'Item the second')
