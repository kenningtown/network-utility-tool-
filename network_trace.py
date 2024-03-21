import subprocess


def trcrouting(dm):       #traceroute
    res = ['traceroute', dm]         #initializing list wih command and domain

    try:
        process = subprocess.run(res,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(process.stdout)         #used subprocess module to print the contents of tracing
    except Exception as ex:
        print(f"Invalid response: {ex}")


 #same procedure for tracepath

def trcpath(domen):
    res = ['tracepath', domen]

    try:
        process = subprocess.run(res,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(process.stdout)
    except Exception as ex:
        print(f"Invalid response: {ex}")



if __name__ == "__main__":
    dmn = input("Enter the address to trace: ") #asking server to trace, then it will print the traceroute and tracepath results.
    trcrouting(dmn)
    trcpath(dmn)

