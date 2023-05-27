from django.test import TestCase
from .models import Account

class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(account_type='Test Account', balance=1000)
        Account.objects.create(account_type='Another Test Account', balance=2000)

    def test_account_balance(self):
        test_account = Account.objects.get(account_type='Test Account')
        another_test_account = Account.objects.get(account_type='Another Test Account')
        self.assertEqual(test_account.balance, 1000)
        self.assertEqual(another_test_account.balance, 2000)
