defmodule GraphqlPubsubWeb.Resolvers.Streams do
  alias GraphqlPubsub.Streams
  alias GraphqlPubsubWeb.Schema.ChangesetErrors


  def observations(_, _, _) do
    {:ok, Streams.list_observations()}
  end

  def create_observation(_, args, _) do
    case Streams.create_observation(args) do
      {:error, changeset} ->
        {:error,
         message: "Could not create observation",
         details: ChangesetErrors.error_details(changeset)
        }

      {:ok, observation} ->
        # publish_observation_change(observation)
        {:ok, observation}
    end
  end


  def create_client_observation(json) do
    case Streams.create_observation(json) do
      {:error, changeset} ->
        {:error,
         message: "Could not create observation",
         details: ChangesetErrors.error_details(changeset)
        }

      {:ok, observation} ->
        IO.puts("observation insert success")
        {:ok, observation}
    end
  end


  defp publish_observation_change(observation) do
    stream_id = Integer.to_string(observation.stream_id)
    target_id = Integer.to_string(observation.target_id)
    topic_id = Enum.join([stream_id, target_id], "-")

    Absinthe.Subscription.publish(
      GraphqlPubsubWeb.Endpoint,
      observation,
      observation_change: topic_id
    )
  end


  def create_subscription(_, args, _) do
    case Streams.find_or_create_subscription(args) do
      {:error, changeset} ->
        {:error,
         message: "Could not create subscription",
         details: ChangesetErrors.error_details(changeset)
        }

        {:ok, subscription} ->
          {:ok, subscription}
    end
  end


  @spec client_subscriptions(any, any, any) :: {:ok, any}
  def client_subscriptions(_, args, _) do
    {:ok, Streams.list_subscription(args)}
  end


end
