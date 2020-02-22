from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver

###### Initialization ######

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('test01.sol') as f:
    source_code = f.read()


# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)

contract_account.balanceOf(user_account)

symbolic_addr = m.make_symbolic_value()
contract_account.balanceOf(symbolic_addr)


# check balance after transfer
symbolic_val = m.make_symbolic_value()
symbolic_to = m.make_symbolic_value()

contract_account.transfer(symbolic_to, symbolic_val)
contract_account.balanceOf(symbolic_to)
contract_account.balanceOf(user_account)

print("TEST01_1! see {}".format(m.workspace))

for state in m.all_states:
    balance_before = state.platform.transactions[1].return_data
    balance_before = ABI.deserialize("uint", balance_before)

    balance_after = state.platform.transactions[-1].return_data
    balance_after = ABI.deserialize("uint", balance_after)

    m.generate_testcase(state, name="TEST01_1")

    state.constrain(Operators.UGT(balance_after, balance_before))
    
    if solver.check(state.constraints):
        m.generate_testcase(state, name="BugFound")
#    else:    
#        m.generate_testcase(state, name="TEST01")

