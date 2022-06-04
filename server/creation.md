mix phx.new satori --live
cd satori
mix phx.gen.live Stream Observation observation source_id:integer stream_id:integer target_id:integer wallet_id:integer value  
// save to router
mix phx.create
mix phx.migrate
mix phx.server
// mix ecto.drop; mix ecto.create; mix ecto.migrate; mix phx.server


----

The immediate need is a self-owned, and therefore cheap pubsub server. that's it.

We need this server to sanction nodes and track their uptime? 
well we don't know how people will get paid, so we don't know what it needs to do yet,
but we at least know each node will be given a unique ID - their wallet public key.
we don't need a server for that.
ok, but we must have a policy for distributing payment so What are the metrics of that policy?

Ideally, subscriptions. but that's a market solution.
this is best because maybe you can predict somthing really accurately but nobody cares about that stream.
then you shouldn't get paid much, huh?

Instead we have to have a currated list of streams that are deemed worthy.
The server knows about and chooses those streams.
And we pay people either on uptime or on accuracy.

uptime everyone gets paid the same amount but its easier to game.
accuracy everyone gets paid slightly variable amounts, but its harder to game.
But accuracy is harder to measure. 
The server basically has to subscribe to all prediction streams. 
mmm that may just be what we have to do until we have a better solution... in phase 3...

that's not the best. we'll probably just do uptime then...
no. we'll be a data aggregator anyway, might as well subscribe to all of them.

Well, what does a better solution look like? 

We record all subscriptions on the blockchain, see.
we'll need to do this anyway so we can build a map of subscriptions.
then you're automatically put into a hashgraph with everyone else subscribed to that thing.
we don't actually need to record everything on chain what we need to know is that you all
agree about who gets paid this round because that's basically it. 
to be continued...

ok, I've slept. 
We are not trying to create decentralized intelligence yet. just distributed.
So it's going to have a centralizing aspect, the server. period.

well not period, I think we can eventually grow out of the server, into a real DAO.
but that's not important to think about at this time.
All we need to think about is how to make it work in a centralized fashion first.

The server will have a list of sanctioned streams, and will gather metrics about those streams.
metrics like, how popular do we think this is? how often does it publish?
what is the entropy profile? how hard is it to predict? etc.
We'll then have a table in the database describing the current (and past) ways we used to value each stream with those metrics as inputs to the formula.
We'll then say, "this stream is very valueable so we'll devide its value up evenly amongst x predictors."
in this way each time we ask the node to predict a new stream it comes with a value, and it's always the same.

Now, they're competing with each other for accuracy though. and they're competing for time.
each and every sanctioned stream has to have at least 3 predictors. If you're the last predictor you get nothing even if you were spot on.
Otherwise the best prediction takes the cake, the cake being, this round, this round being the latest observation.

How to stop collusion? well first of all the incentive to collude is low. you're saving your compute power. thats it.
But I get it, if you wan collude without end, you can steal earnings without end.
That's not really a possibility because if all predictions go to shit, ban everyone that makes shit predictions.
So right off the bat, with this centralized system, theres only so much collusion you can acheive. at some point its really obvious.

But how do we minimize it still? Probably the best way is to have an upfront cost.
This fits naturally into the requirement that publishing on streamr costs 10.
most computers will predict multiple streams. so you might spend 30-1000. 
so now you can't do sybl attacks because you can't just spin up nodes for free.

if a computer goes offline, we have to eventually remove it from the group. and add someone new to the predictors on that stream.

I really do think this is the best we can do right now. Now, we should have like an incentive structure for sharing if we're going to have an upfront cost.
If we charge twice as much as we expect for publication costs we can split that extra with the referrer.
$100 per node means $50 credit for publication costs, $25 referral fee, $25 revenue.

