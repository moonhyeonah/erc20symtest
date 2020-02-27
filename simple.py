from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators
from manticore.core.smtlib.solver import Z3Solver
from manticore.core.manticore import ManticoreBase

###### Initialization ######
#ManticoreBase.verbosity(5)

m = ManticoreEVM()
solver = Z3Solver.instance()

with open('simple.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)
#tmp_account1 = m.create_account(balance=1000)
#tmp_account2 = m.create_account(balance=1000)

#print(hex(int(user_account)))
#print(hex(int(tmp_account1)))
#print(hex(int(tmp_account2)))
#print("-------\n")

from_account = m.make_symbolic_value()
to_account = m.make_symbolic_value()
m.constrain(from_account != to_account)

#print(hex(int(user_account)))
#print(hex(int(from_account)))
#print(hex(int(to_account)))

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0)
contract_account.balanceOf(to_account, caller=user_account)
contract_account.balanceOf(from_account, caller=user_account)
contract_account.balanceOf(user_account, caller=user_account)

symbolic_val1 = m.make_symbolic_value()
#m.constrain(symbolic_val1 > 100)

contract_account.transfer(to_account, symbolic_val1, caller=from_account)
contract_account.balanceOf(user_account, caller=user_account)
contract_account.balanceOf(from_account, caller=user_account)
contract_account.balanceOf(to_account, caller=user_account)

for state in m.ready_states:    
   
    #for tx in state.platform.transactions:
    #    print("From address: (0x%x) \n" % (tx.caller))
    #print("********\n")
        
    balance_before = state.platform.transactions[1].return_data
    balance_before = ABI.deserialize("uint", balance_before)

    balance_after = state.platform.transactions[-1].return_data
    balance_after = ABI.deserialize("uint", balance_after)

    state.constrain(Operators.ULT(balance_before, balance_after))

    if solver.check(state.constraints):
        print("Found! see {}".format(m.workspace))
        m.generate_testcase(state, "Found")
