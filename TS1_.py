from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

###### Initialization ######

m = ManticoreEVM()
with open('test01.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)

contract_account.balanceOf(user_account)

symbolic_addr = m.make_symbolic_value()
contract_account.balanceOf(symbolic_addr)

for state in m.all_states:
    m.generate_testcase(state, 'TEST01')

