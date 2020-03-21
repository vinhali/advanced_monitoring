import sys

def starting(user, frequency, playbook, customer, host):
        print("**********************************************************************")
        print('''Starting with config:
        User: {0}
        Frequency: {1}
        Playbook: {2}
        Customer: {3}
        Host: {4}'''.format(user,frequency,playbook,customer,host))
        print("**********************************************************************")

if __name__ == "__main__":
        starting(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
