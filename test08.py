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
m.create_account(balance=1000)
m.create_account(balance=1000)
from_account = m.make_symbolic_value()
to_account = m.make_symbolic_value()
m.constrain(from_account != to_account)
#print("from_account : 0x%x (%d)"%(from_account, from_account))
#print("to_account : 0x%x (%d)"%(to_account, to_account))

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)
contract_account.balanceOf(to_account, caller=user_account)
contract_account.balanceOf(from_account, caller=user_account)

symbolic_val1 = m.make_symbolic_value()

contract_account.transfer(to_account, symbolic_val1, caller=from_account)
contract_account.balanceOf(from_account, caller=user_account)
contract_account.balanceOf(to_account, caller=user_account)

for state in m.ready_states:    
    
    input = state.input_symbols[0]
    input = Operators.CONCAT(256, *input[4:36])
    print("input0 : {}".format(input))

    input = state.input_symbols[1]
    input = Operators.CONCAT(256, *input[4:36])
    print("input1 : {}".format(input))

    input = state.input_symbols[2]
    input = Operators.CONCAT(256, *input[4:36])
    print("input2 : {}".format(input))

    input = state.input_symbols[3]
    input = Operators.CONCAT(256, *input[4:36])
    print("input3 : {}".format(input))
    
    input = state.input_symbols[4]
    input = Operators.CONCAT(256, *input[4:36])
    print("input4 : {}".format(input))
    
    balance_before = state.platform.transactions[1].return_data
    balance_before = ABI.deserialize("uint", balance_before)

    balance_after = state.platform.transactions[-1].return_data
    balance_after = ABI.deserialize("uint", balance_after)

    state.constrain(Operators.ULT(balance_before, balance_after))

    if solver.check(state.constraints):
        print("Overflow found! see {}".format(m.workspace))
        m.generate_testcase(state, "OverflowFound")
