from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver
from manticore.core.manticore import ManticoreBase

#ManticoreBase.verbosity(5)

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('AP2.sol') as f:
    source_code = f.read()

user_account = m.create_account(balance=1000)

spender_account = m.make_symbolic_value()
m.constrain(spender_account != user_account)

symbolic_to = m.make_symbolic_value()
m.constrain(symbolic_to != user_account)

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0, args=None)
#contract_account.balanceOf(spender_account, caller=user_account)

contract_account.balanceOf(user_account, caller=user_account)
contract_account.allowance(user_account, spender_account)

symbolic_approve = m.make_symbolic_value()
contract_account.approve(spender_account, symbolic_approve, caller=user_account)

#for state in m.ready_states:
#    val = state.platform.transactions[-1].return_data
#    val = ABI.deserialize("uint", val)

symbolic_val = m.make_symbolic_value()
#m.constrain(symbolic_val > val)
contract_account.transferFrom(user_account, symbolic_to, symbolic_val, caller=spender_account)

contract_account.balanceOf(symbolic_to, caller=user_account)
contract_account.balanceOf(user_account, caller=user_account)
contract_account.allowance(user_account, spender_account)

for state in m.all_states:
    print("TF1! see {}".format(m.workspace))
    m.generate_testcase(state, name="TF1")

