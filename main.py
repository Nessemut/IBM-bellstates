from IBMQuantumExperience import IBMQuantumExperience
from math import sqrt
from time import sleep
from sys import exit

qasm = 'OPENQASM 2.0;' \
       '\n\ninclude "qelib1.inc";' \
       '\nqreg q[2];' \
       '\ncreg c[2];' \
       '\nh q[0];' \
       '\ncx q[0],q[1];' \
       '\nmeasure q[0] -> c[0];' \
       '\nmeasure q[1] -> c[1];\n'

runs = 0
ones = 0


def get_probability():
    p1 = round(sqrt(ones/runs), 3)
    p0 = round(sqrt((runs - ones)/runs), 3)
    return str(p1) + "|00> + " + str(p0) + "|11>"


def run():
    try:
        apikey = open("apikey.txt", "r").read()
    except FileNotFoundError:
        print("Please put an 'apikey.txt' file in the program root with your IBM's API key")
        exit()
    try:
        api = IBMQuantumExperience(apikey)
        resp = api.run_experiment(
            qasm,
            'simulator',
            1,
            name=None,
            timeout=180
        )

        measurement = resp['result']['measure']['labels'][0]
        return measurement
    except TimeoutError:
        print("Connection aborted, waiting for reconnection to simulator...")
        sleep(10)


while True:
    res = run()
    runs += 1

    if '1' in res:
        ones += 1

    print('Run {}: measured |{}>     p = ({})'.format(runs, res, get_probability()))
