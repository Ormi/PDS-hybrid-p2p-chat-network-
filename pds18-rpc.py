import argparse

parser = argparse.ArgumentParser(description="Hybrid p2p chat application RPC module")
group = parser.add_mutually_exclusive_group()
parser.add_argument("--id", type=int, required=True help="--id us unique identifier of peer or node, which RPC must send command")
group.add_argument("--peer", required=True help="Command for instance of peer")
group.add_argument("--node", required=True help="Command for instance of server")
parser.add_argument("--command", required=True help="with list of parameter specifies commands and parameters related to given RCP call")        
args = parser.parse_args()
print(args)

# ./pds18-rpc --id <identifikátor> <"--peer"|"--node"> --command <příkaz> --<parametr1> <hodnota_parametru1> ...
