from datetime import datetime
from django.test import TestCase

from medimg.models import Todo, TodoList

class TodoTestCase(TestCase):

    def setUp(self):
        self.todoList =TodoList()
        self.todoList.name ='test todo list '
        self.todoList.save()


    def test_create_todo(self):
        nb_todo_before_add = Todo.objects.count()
        new_todo =Todo()
        new_todo.title ='achat eau'
        new_todo.due_date=datetime.today()
        new_todo.favorite=True
        new_todo.completed=False
        new_todo.list =self.todoList

        new_todo.save()

        nb_todo_after_add = Todo.objects.count()
        self.assertTrue(nb_todo_after_add == nb_todo_before_add +1)

