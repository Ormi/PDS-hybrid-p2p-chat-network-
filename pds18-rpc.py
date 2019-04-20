###############################################################################
# Project for PDS ( Data Communications, Computer Networks and Protocols )
# @file pds18-rpc.py (3)
# @author Michal Ormos (xormos00)
# @email xormos00@stud.fit.vutbr.cz
# @date April 2019
###############################################################################


import argparse

parser = argparse.ArgumentParser(description="Hybrid p2p chat application RPC module")
group = parser.add_mutually_exclusive_group()
command_group = parser.add_mutually_exclusive_group()
parser.add_argument("--id", type=int, required=True, help="--id us unique identifier of peer or node, which RPC must send command")
group.add_argument("--peer", help="Command for instance of peer")
group.add_argument("--node", help="Command for instance of server")

command_group.add_argument("message", help="Command for instance of server")
parser.add_argument("--from", required="message", help="Command for instance of server")
parser.add_argument("--to", required="message", help="Command for instance of server")
parser.add_argument("--message", required="message", help="Command for instance of server")

command_group.add_argument("--getlist", help="Command for instance of server")
command_group.add_argument("--peers", help="Command for instance of server")
command_group.add_argument("--reconnect", help="Command for instance of server")
command_group.add_argument("--database", help="Command for instance of server")
command_group.add_argument("--neighbors", help="Command for instance of server")
command_group.add_argument("--connect", help="Command for instance of server")
command_group.add_argument("--discover", help="Command for instance of server")
command_group.add_argument("--sync", help="Command for instance of server")

parser.add_argument("--command", required=True, help="with list of parameter specifies commands and parameters related to given RCP call")        
args = parser.parse_args()
print(args)

# ./pds18-rpc --id <identifikátor> <"--peer"|"--node"> --command <příkaz> --<parametr1> <hodnota_parametru1> ...

# --peer --command message --from <username1> --to <username2> --message <zpráva>, který se pokusí odeslat chat zprávu
# --peer --command getlist, který vynutí aktualizaci seznamu v síti známých peerů, tj. odešle zprávu GETLIST a nechá si ji potvrdit
# --peer --command peers, který zobrazí aktuální seznam peerů v síti, tj. peer si s node vymění zprávy GETLIST a LIST, přičemž obsah zprávy LIST vypíše
# --peer --command reconnect --reg-ipv4 <IP> --reg-port <port>, který se odpojí od současného registračního uzlu (nulové HELLO) a připojí se k uzlu specifikovaném v parametrech

# --node --command database, který zobrazí aktuální databázi peerů a jejich mapování
# --node --command neighbors, který zobrazí seznam aktuálních sousedů registračního uzlu
# --node --command connect --reg-ipv4 <IP> --reg-port <port>, který se pokusí navázat sousedství s novým registračním uzlem
# --node --command disconnect, který zruší sousedství se všemi uzly (stáhne z jejich DB své autoritativní záznamy) a odpojí node od sítě
# --node --command sync, která vynutí synchronizaci DB s uzly, se kterými node aktuálně sousedí