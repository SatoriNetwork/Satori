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
        publish_observation_change(observation)
        {:ok, observation}
    end
  end


  defp publish_observation_change(observation) do
    s_id = Integer.to_string(observation.stream_id)
    t_id = Integer.to_string(observation.target_id)
    topic_id = Enum.join([s_id, t_id], "-")

    Absinthe.Subscription.publish(
      GraphqlPubsubWeb.Endpoint,
      observation,
      observation_change: topic_id
    )
  end
end
