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
user_account = m.create_account(balance=1000)
contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)

contract_account.balanceOf(user_account)

# check balance after transfer
symbolic_val = 19 #m.make_symbolic_value()
#m.constrain(symbolic_val >= 0)
#m.constrain(symbolic_val < 100)
symbolic_to = m.make_symbolic_value(name="ADDRESS")
m.constrain(symbolic_to != user_account)

contract_account.transfer(symbolic_to, symbolic_val, caller=user_account)
contract_account.balanceOf(symbolic_to)
contract_account.balanceOf(user_account)

#print("TEST08! see {}".format(m.workspace))

for state in m.all_states:
    state.constrain(symbolic_to != user_account)
    if solver.check(state.constraints):
        print("TEST08! see {}".format(m.workspace))
        m.generate_testcase(state, name="TEST08")
#    balance_before = state.platform.transactions[1].return_data
#    balance_before = ABI.deserialize("uint", balance_before)

#    balance_after = state.platform.transactions[-1].return_data
#    balance_after = ABI.deserialize("uint", balance_after)

#    m.generate_testcase(state, name="TEST08")

#    state.constrain(Operators.UGT(balance_after, balance_before))
    
#    if solver.check(state.constraints):
#        m.generate_testcase(state, name="BugFound")

