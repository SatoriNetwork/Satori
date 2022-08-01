# to be called by elixir since verification works well in python 
# https://medium.com/stuart-engineering/how-we-use-python-within-elixir-486eb4d266f9

#from ravencoin.signmessage import RavencoinMessage, VerifyMessage
#
#def generateAddress(publicKey: str):
#    from ravencoin.wallet import P2PKHRavencoinAddress
#    from ravencoin.core.key import CPubKey
#    return str(
#        P2PKHRavencoinAddress.from_pubkey(
#            CPubKey(
#                bytearray.fromhex(
#                    publicKey))))
#
#def verify(message:'str|RavencoinMessage', signature:'bytes|str', publicKey:str=None, address:str=None):
#    return VerifyMessage(
#        address or generateAddress(publicKey),
#        RavencoinMessage(message) if isinstance(message, str) else message,
#        signature if isinstance(signature, bytes) else signature.encode())

# to be used by elixir thusly:
# 1. get the path somehow or hardcode it or whatever:
#path = [:code.lib_dir(:satori), "utils"] |> Path.join()  
#"c:/repos/Satori/server/satori/_build/dev/lib/satori/utils/verify"
# 2. get the pid?
#{:ok, pid} = :python.start([{:python_path, to_charlist(path)}, {:python, 'python3'}])
# 3. call the function
#result = :python.call(pid, :verify, :generateAddress, ["035cec31f0379de2a13fe4bd6c1c7fd705052d8bf3de8a68df6f2b2092cb5a7dcb"])
#result = :python.call(pid, :verify, :verify, ["message", "IPE/G97TLAV9KkkYXHCIVOL8rQRowN6Ab7omLTbnT4ZHKNdUh5gJPlMY+fZycOMS+V64bhHJfd4CPn7459jVt2c=", "035cec31f0379de2a13fe4bd6c1c7fd705052d8bf3de8a68df6f2b2092cb5a7dcb"])

#Actually we can't call this because we can't import using this method, and we're not going to bring the entire python-ravencoinlib codebase into the file so we must make it a cli utility
#So, the code above is dead, and the utility in satori has been created, which means satori must be installed on the server, or the cli portion must be installed on the server:

#System.cmd("satori", ["verify", "message", "IPE/G97TLAV9KkkYXHCIVOL8rQRowN6Ab7omLTbnT4ZHKNdUh5gJPlMY+fZycOMS+V64bhHJfd4CPn7459jVt2c=", "035cec31f0379de2a13fe4bd6c1c7fd705052d8bf3de8a68df6f2b2092cb5a7dcb"])
#{"True\r\n", 0}

