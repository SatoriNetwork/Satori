mix phx.gen.live Accounts User users name:string age:string

mix phx.gen.live Wallets Wallet wallets user_id:int address:string scripthash:string



mix phx.gen.live Devices Device devices name:string cpu:string disk:int bandwidth:string ram:int wallet_id:int

mix phx.gen.live Subscribers Subscriber subscribers stream_id:int device_id:int target_id:int

mix phx.gen.live Streams Stream streams wallet_id:int source_name:string name:string cadence:string sanctioned:bool

mix phx.gen.live Observations Observation observations stream_id:int wallet_id:int target_id:int value:string

mix phx.gen.live Targets Target targets name:string
