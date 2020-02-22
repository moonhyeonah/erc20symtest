from manticore.ethereum import ManticoreEVM, ABI
from manticore.core.smtlib import Operators, solver

###### Initialization ######

m = ManticoreEVM()
with open('cons_with_args.sol') as f:
    source_code = f.read()

# Create one user account
# And deploy the contract
user_account = m.create_account(balance=1000)

contract_account = m.solidity_create_contract(source_code, owner=user_account, balance=0, args="(uint,uint)")

contract_account.totalSupply()

print("TEST03! see {}".format(m.workspace))
for state in m.all_states:
    m.generate_testcase(state, name="TEST03")

