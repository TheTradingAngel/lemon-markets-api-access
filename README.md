# Lemon Markets API Access

This is a Python SDK for accessing the Lemon Markets API.
API documentation can be found here: https://documentation.lemon.markets/

## Installation

```
git clone https://github.com/LinusReuter/lemon-markets-api-access.git
python setup.py install
```


## Usage

### Authentication

For getting started the account must be initialized. 
The account is needed for further requests.
Your access_token is automatically updated when it expires.

```python
from lemon_markets.account import Account

account = Account(your_client_id, your_client_secret)

#for seeing your accsess token
print(account.access_token)
```

### State and Space


```python
from lemon_markets.state import State

state = State(account)

#get the balance of the state (all money not given to spaces)
print(state.balance) 

#get your space (because your client ID is linked to a Space the request "list Spaces" only contains one space.)
space = state.spaces[0]
print(space.state) #the state of the space as dict like in the API response.
#the elements of the state as floats:
print(space.balance)
print(space.cash_to_invest)
```

### Instruments
```python
from lemon_markets.paper_money.instrument import *

#getting a list of all Instruments matching the query params 
#(all arguments are an option and not needed)
instruments = Instruments(account).list_instruments(tradable=true/false, search="Name/Title, WKN, Symbol or ISIN", currency="", type="one of the following:" ("stock", "bond", "fond", "ETF" or "warrant"))

#get a singe instrument by isin:
instrument = Instruments(account).get_instrument(isin="")

#to get the information of an instrument use:
instrument.isin
instrument.wkn
instrument.name
instrument.title
instrument.type
instrument.symbol
instrument.currency
instrument.tradable
instrument.trading_venues
```

### Time Helper
All times in this library are stored as timezone aware datetime objects. 
Furthermore, datetime objects are needed for passing a time to a library function, such as creating an order. 
```python
from lemon_markets.helpers.time_helper import *

current_time()  # returns the current time as a timezone aware datetime object.
time(year= , month= , day= , hour= , minute= , second= )  # all params require an integer and are optional. If paramameter is not set the current year/month/... is used. Returns a timezone aware datetime object. 

# mostly for internal use:
datetime_to_timestamp(datetime) # creates an UTC timestamp from the given datetime objects. 
timestamp_to_datetime(timestamp) # creates an datetime object with local timezone from the given UTC timestamp.

```


### Orders
```python
from lemon_markets.paper_money.order import *

# Initialise the Orders Class
orders = Orders(account=acc, space=space)
print(orders.orders) # see all created and retrieved orders sorted in dicts by status. 
# the Structure of the orders.orders dict:
# {'INACTIVE': {'order_uuid': Order}, 
#  'ACTIVATED': {'order_uuid': Order}, 
#  'IN_PROGRESS': {'order_uuid': Order}, 
#  'EXECUTED': {'order_uuid': Order}, 
#  'DELETED': {'order_uuid': Order}, 
#  'EXPIRED': {'order_uuid': Order}}

# create an order:
order = orders.create_order(instrument=, valid_until=, quantity=, side=)  # creates and order stores it in the orders.orders dict and returns the order

# activate an order:
orders.activate_order(order)

# update the status and data of an order:
orders.update_order(order)

#delete an order:
orders.delete_order(order)

# fill the orders.orders dict by listing your orders
orders.get_orders(created_at_until=, created_at_from=, side=, type= , status=)  # all params optional

# clean the orders.orders dict:
orders.clean_orders()  # removes all executed, deleted or expired orders in the orders dict
```