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
    Absinthe.Subscription.publish(
      GraphqlPubsubWeb.Endpoint,
      observation,
      observation_change: observation.id
    )
  end
end
