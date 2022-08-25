defmodule GraphqlPubsub.Streams do

  import Ecto.Query, warn: false
  alias GraphqlPubsub.Repo

  alias GraphqlPubsub.Streams.{Observation}
  # alias GraphqlPubsub.Accounts.User



  def list_observations do
    Repo.all(Observation)
  end



  def create_observation(attrs) do
    %Observation{}
    |> Observation.changeset(attrs)
    |> Repo.insert()
  end

end
