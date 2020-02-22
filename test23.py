from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver

###### Initialization ######

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('test22.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)

symbolic_spender = m.make_symbolic_value(name="ADDRESS")
m.constrain(symbolic_spender != user_account)

symbolic_val = m.make_symbolic_value()

contract_account.allowance(user_account,symbolic_spender)
contract_account.approve(symbolic_spender, symbolic_val, caller=user_account)
contract_account.allowance(user_account,symbolic_spender)

print("TEST23! see {}".format(m.workspace))

for state in m.all_states:
    m.generate_testcase(state, name="TEST23")

