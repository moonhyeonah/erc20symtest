from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver
from manticore.core.manticore import ManticoreBase

###### Initialization ######
#ManticoreBase.verbosity(5)

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('test08.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
#from_account = m.create_account(balance=1000)
m.create_account(balance=1000)
m.create_account(balance=1000)
from_account = m.make_symbolic_value()
to_account = m.make_symbolic_value()
m.constrain(from_account != to_account)

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)
contract_account.balanceOf(to_account)
contract_account.balanceOf(from_account)

symbolic_val1 = m.make_symbolic_value()

contract_account.transfer(to_account, symbolic_val1, caller=from_account)
contract_account.balanceOf(from_account)
contract_account.balanceOf(to_account)

for state in m.ready_states:
    balance_before = state.platform.transactions[1].return_data
    balance_before = ABI.deserialize("uint", balance_before)

    balance_after = state.platform.transactions[-1].return_data
    balance_after = ABI.deserialize("uint", balance_after)

    state.constrain(Operators.ULT(balance_before, balance_after))

    if solver.check(state.constraints):
        print("Overflow found! see {}".format(m.workspace))
        m.generate_testcase(state, "OverflowFound")

