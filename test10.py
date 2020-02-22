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
user_account = m.create_account(balance=100)
to_account = m.create_account(balance=101)

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)
contract_account.balanceOf(to_account)
contract_account.balanceOf(user_account)

for state in m.ready_states:
    val = state.platform.transactions[-1].return_data
    val = ABI.deserialize("uint", val)

symbolic_val = m.make_symbolic_value()
m.constrain(symbolic_val > val)

contract_account.transfer(to_account, symbolic_val, caller=user_account)

contract_account.balanceOf(user_account)
contract_account.balanceOf(to_account)


for state in m.all_states:
    print("TEST10! see {}".format(m.workspace))
    m.generate_testcase(state, name="TEST10")

