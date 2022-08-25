defmodule GraphqlPubsubWeb.Schema.Schema do
  use Absinthe.Schema

  alias GraphqlPubsubWeb.Resolvers


  mutation do
    @desc "Create an observation"
    field :create_observation, :observation do
      arg :wallet_id, non_null(:integer)
      arg :stream_id, non_null(:integer)
      arg :target_id, non_null(:integer)
      arg :value, non_null(:string)
      resolve &Resolvers.Streams.create_observation/3
    end
  end


  subscription do
    @desc "Subscribe to observation changes"
    field :observation_change, :observation do
      arg :stream_id, non_null(:integer)
      arg :target_id, non_null(:integer)
      config fn args, _res ->
        s_id = Integer.to_string(args.stream_id)
        t_id = Integer.to_string(args.target_id)
        topic_id = Enum.join([s_id, t_id], "-")
        {:ok, topic: topic_id}
      end
    end
  end


  query do
    @desc "Get an observation"
    field :observation, :observation do
      arg :stream_id, non_null(:integer)
      arg :target_id, non_null(:integer)
      resolve &Resolvers.Streams.observations/3
    end
  end


  object :observation do
    field :id, non_null(:id)
    field :wallet_id, non_null(:integer)
    field :stream_id, non_null(:integer)
    field :target_id, non_null(:integer)
    field :value, non_null(:string)
  end


end
