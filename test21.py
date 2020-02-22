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
symbolic_spender = m.create_account(balance=101)

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)
contract_account.balanceOf(user_account)

for state in m.ready_states:
    val = state.platform.transactions[-1].return_data
    val = ABI.deserialize("uint", val)

symbolic_val = m.make_symbolic_value()
m.constrain(symbolic_val > 0)
m.constrain(symbolic_val <= val)

contract_account.allowance(user_account,symbolic_spender)
contract_account.approve(symbolic_spender, symbolic_val, caller=user_account)
contract_account.allowance(user_account,symbolic_spender)


for state in m.all_states:
    print("TEST21! see {}".format(m.workspace))
    m.generate_testcase(state, name="TEST21")

