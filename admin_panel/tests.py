from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import ChatConversation, Message, PredefinedMessage, Administrateur, AdministrateurPrincipal, ChatbotUser

User = get_user_model()

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))

    def test_create_super_admin(self):
        super_admin = User.objects.create_user(username='superadmin', email='superadmin@example.com', password='password123', is_super_admin=True)
        self.assertTrue(super_admin.is_super_admin)

class ChatbotUserModelTest(TestCase):

    def test_create_chatbot_user(self):
        chatbot_user = ChatbotUser.objects.create(name='Chatbot', email='chatbot@example.com', password=make_password('password123'))
        self.assertEqual(chatbot_user.name, 'Chatbot')
        self.assertTrue(chatbot_user.check_password('password123'))

class AdministrateurModelTest(TestCase):

    def test_create_administrateur(self):
        admin = Administrateur.objects.create(name='Admin', email='admin@example.com', password=make_password('password123'))
        self.assertEqual(admin.name, 'Admin')
        self.assertTrue(admin.check_password('password123'))

class AdministrateurPrincipalModelTest(TestCase):

    def test_create_administrateur_principal(self):
        principal_admin = AdministrateurPrincipal.objects.create(name='Principal Admin', email='principaladmin@example.com', password=make_password('password123'))
        self.assertEqual(principal_admin.name, 'Principal Admin')
        self.assertTrue(principal_admin.check_password('password123'))

class ChatConversationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
    
    def test_create_conversation(self):
        conversation = ChatConversation.objects.create(user=self.user, content='Initial content')
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.content, 'Initial content')

class MessageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.chatbot_user = ChatbotUser.objects.create(name='Chatbot', email='chatbot@example.com', password=make_password('password123'))
        self.conversation = ChatConversation.objects.create(user=self.user, content='Initial content')

    def test_create_message_user_author(self):
        message = Message.objects.create(conversation=self.conversation, author_user=self.user, content='Test message')
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.author_user, self.user)
        self.assertIsNone(message.author_chatbot)
        self.assertEqual(message.content, 'Test message')

    def test_create_message_chatbot_author(self):
        message = Message.objects.create(conversation=self.conversation, author_chatbot=self.chatbot_user, content='Test message')
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.author_chatbot, self.chatbot_user)
        self.assertIsNone(message.author_user)
        self.assertEqual(message.content, 'Test message')

    def test_update_message_content(self):
        message = Message.objects.create(conversation=self.conversation, author_user=self.user, content='Test message')
        message.content = 'Updated content'
        message.save()
        self.assertEqual(message.content, 'Updated content')

class PredefinedMessageModelTest(TestCase):

    def test_create_predefined_message(self):
        predefined_message = PredefinedMessage.objects.create(title='Greeting', content='Hello, how can I help you?')
        self.assertEqual(predefined_message.title, 'Greeting')
        self.assertEqual(predefined_message.content, 'Hello, how can I help you?')

