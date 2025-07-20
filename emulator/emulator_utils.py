# emulator utils

def print_state(state):
    '''print the values in all the registers the pc'''
    print(f"registers:\n")
    for i in range(32):
        print(f"x{i} = {state['registers'][i]}")
    print(f"\n ~~~ \n")
    print(f"pc={state['pc']}")

