from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

m = ManticoreEVM()
with open('maxfunction.sol') as f:
    source_code = f.read()

user_account = m.create_account(balance=1000)
contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)

symbolic_x = m.make_symbolic_value()
symbolic_y = m.make_symbolic_value()
symbolic_z = m.make_symbolic_value()
#m.constrain(symbolic_x > symbolic_y)

#contract_account.maxOf(symbolic_x, symbolic_y, symbolic_z)
contract_account.maxOfList(symbolic_x, symbolic_y, symbolic_z)

print("maxfunction.py! see {}".format(m.workspace))

for state in m.all_states:
    m.generate_testcase(state, 'MaxFunction')
