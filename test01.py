from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver

###### Initialization ######

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('test08.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account1 = m.create_account(balance=100)
user_account2 = m.create_account(balance=101)

contract_account = m.solidity_create_contract(source_code, owner=user_account1, balance=0)

contract_account.balanceOf(user_account1)
contract_account.balanceOf(user_account2)

for state in m.all_states:
    print("TEST01! see {}".format(m.workspace))
    m.generate_testcase(state, name="TEST01")
