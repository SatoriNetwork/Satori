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

    # devices technically subscribe to a single target on a stream
    @desc "Create target subscription"
    field :create_subscription, :target_subscription do
      arg :stream_id, non_null(:integer)
      arg :device_id, non_null(:integer)
      arg :target_id, non_null(:integer)
      resolve &Resolvers.Streams.create_subscription/3
    end

  end


  # subscription do
  #   @desc "Subscribe to observation changes"
  #   field :observation_change, :observation do
  #     arg :stream_id, non_null(:integer)
  #     arg :target_id, non_null(:integer)
  #     config fn args, _res ->
  #       stream_id = Integer.to_string(args.stream_id)
  #       target_id = Integer.to_string(args.target_id)
  #       topic_id = Enum.join([stream_id, target_id], "-")
  #       {:ok, topic: topic_id}
  #     end
  #   end
  # end


  query do
    @desc "Get an observation"
    field :observation, :observation do
      arg :stream_id, non_null(:integer)
      arg :target_id, non_null(:integer)
      resolve &Resolvers.Streams.observations/3
    end


    @desc "Get list of client subscriptions"
    field :client_subscriptions, list_of(:target_subscription) do
      arg :limit, :integer
      arg :order, type: :sort_order, default_value: :desc
      arg :device_id, :integer
      resolve &Resolvers.Streams.client_subscriptions/3
    end

  end


  object :observation do
    field :id, non_null(:id)
    field :wallet_id, non_null(:integer)
    field :stream_id, non_null(:integer)
    field :target_id, non_null(:integer)
    field :value, non_null(:string)
  end


  object :target_subscription do
    field :id, non_null(:id)
    field :stream_id, non_null(:integer)
    field :device_id, non_null(:integer)
    field :target_id, non_null(:integer)
  end



  #
  # Input Object Types
  #

  enum :sort_order do
    value :asc
    value :desc
  end


end
