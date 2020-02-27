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

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0, args=None)
#contract_account.balanceOf(spender_account, caller=user_account)
contract_account.balanceOf(user_account, caller=user_account)

for state in m.ready_states:
    val = state.platform.transactions[-1].return_data
    val = ABI.deserialize("uint", val)

symbolic_val = m.make_symbolic_value()
m.constrain(symbolic_val > val)

contract_account.allowance(user_account,spender_account)
contract_account.approve(spender_account, symbolic_val, caller=user_account)
contract_account.allowance(user_account,spender_account)

for state in m.all_states:
    print("AP2! see {}".format(m.workspace))
    m.generate_testcase(state, name="AP2")

