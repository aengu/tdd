from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name = 'project1',
            budget = 10000
        )

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')
    
    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')
    
    def test_project_detail_POST_adds_new_expense(self):
        Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        self.assertEqual(response.status_code, 302) # 302 Found: 요청한 리소스가 임시적으로 다른 위치에 있음.
        self.assertEqual(self.project1.expenses.first().title, 'expense1')
    
    def test_projcet_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.count(), 0)
    
    def test_project_detail_DELETE_deletes_expense(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category =  category1
        )
        
        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1
        }))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.project1.expenses.count(), 0)
    
    def test_project_detail_DELETE_no_id(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category =  category1
        )
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.project1.expenses.count(), 1)
    
    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'project2',
            'budget': 2000,
            'categoriesString': 'design,development'
        })
        self.assertEqual(response.status_code, 302)
        
        project2 = Project.objects.get(id=2)
        self.assertAlmostEqual(project2.name, 'project2')
        first_category = Category.objects.get(id=1)
        self.assertAlmostEqual(first_category.name, 'design')
        self.assertAlmostEqual(first_category.project, project2)
        second_category = Category.objects.get(id=2)
        self.assertAlmostEqual(second_category.name, 'development')
        self.assertAlmostEqual(second_category.project, project2)

