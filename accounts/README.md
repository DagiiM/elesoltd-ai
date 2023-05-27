
### Endpoints ###

GET /accounts/{id}/ - Retrieve a specific account by ID
PUT /accounts/{id}/ - Update a specific account by ID
PATCH /accounts/{id}/ - Partially update a specific account by ID
POST /accounts/{id}/deposit/ - Deposit to a specific account by ID
POST /accounts/{id}/transfer/ - Transfer to a specific account by ID
POST /accounts/{id}/withdraw/ - Withdraw from a specific account by ID
GET /accounts/{id}/balance/ - Retrieve the balance of a specific account by ID
GET /accounts/{id}/transactions/ - Retrieve the mini statement of a specific account by ID
GET /accounts/{id}/statement/ - Generate a statement (up to 100 transactions) for a specific account by ID, with optional start and end dates


GET /accounts/: retrieve a list of all accounts
POST /accounts/: create a new account
GET /accounts/{pk}/: retrieve an account with a specific primary key (pk)
PUT /accounts/{pk}/: update an account with a specific primary key (pk)
PATCH /accounts/{pk}/: partially update an account with a specific primary key (pk)
DELETE /accounts/{pk}/: delete an account with a specific primary key (pk)
GET /accounts/{pk}/cards/: retrieve a list of cards associated with an account with a specific primary key (pk)
POST /accounts/{pk}/cards/: create a new card associated with an account with a specific primary key (pk)
GET /accounts/{pk}/cards/{card_pk}/: retrieve a card with a specific primary key (card_pk) associated with an account with a specific primary key (pk)
PUT /accounts/{pk}/cards/{card_pk}/: update a card with a specific primary key (card_pk) associated with an account with a specific primary key (pk)
PATCH /accounts/{pk}/cards/{card_pk}/: partially update a card with a specific primary key (card_pk) associated with an account with a specific primary key (pk)
DELETE /accounts/{pk}/cards/{card_pk}/: delete a card with a specific primary key (card_pk) associated with an account with a specific primary key (pk)


"""
This module provides models for managing bank accounts and transactions.

Classes:
- Account: Model representing a bank account.
- AccountManager: Manager for the Account model, providing custom methods for creating accounts and generating account numbers.
- Transaction: Model representing a transaction (deposit, withdrawal, or transfer) on a bank account.
- TransactionManager: Manager for the Transaction model, providing custom methods for creating transactions.

Signals:
- create_account: Signal that creates an Account object when a User object is created.

Functions:
- send_activation_email: Function that sends an activation email to a newly created user.

Usage:
1. Import the models and functions you need from this module, for example:
    from bank.models import Account, Transaction, send_activation_email

2. Create new accounts using the create_account method of the AccountManager, for example:
    account = Account.objects.create_account(user=user, account_type='normal', balance=Decimal('0.00'))

3. Perform transactions on accounts using the deposit, withdraw, and transfer methods of the Account model, for example:
    transaction = account.deposit(amount=Decimal('100.00'), description='Initial deposit')

4. Retrieve transaction history using the mini_statement and generate_statement methods of the Account model, for example:
    transactions = account.mini_statement(no_of_transactions=10)

5. Listen for the create_account signal to perform additional actions when a user is created, for example:
    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
            send_activation_email(user=instance, email=instance.email)
"""
