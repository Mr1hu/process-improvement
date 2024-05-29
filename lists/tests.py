from django.test import TestCase
from lists.views import home_page 
from django.http import HttpRequest
from lists.models import Item
from django.shortcuts import render, redirect

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text']) #(2)
        return redirect('/')
    
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.test = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'The second list item')

class HomePageTest(TestCase):

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        response = self.client.get('/')
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1) #(1)
        new_item = Item.objects.first() #(2)
        self.assertEqual(new_item.text, 'A new list item') #(3)

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
    
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
           
    def test_home_page_return_correct_html(self):
        request = HttpRequest()   #(1)
        response = home_page(request)   #(2)
        html = response.content.decode('utf8')  #(3)
        self.assertTrue(html.startswith('<html>'))   #(4)
        self.assertIn('<title>To-Do lists</title>', html)  #(5)
        self.assertTrue(html.endswith('</html>'))
# Create your tests here.
