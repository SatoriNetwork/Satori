mix phx.new satori --live
cd satori
mix phx.gen.live Stream Observation observation source_id:integer stream_id:integer target_id:integer wallet_id:integer value  
// save to router
mix phx.create
mix phx.migrate
mix phx.server
// mix ecto.drop; mix ecto.create; mix ecto.migrate; mix phx.server
