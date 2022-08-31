defmodule GraphqlPubsub.Streams.Observation do
  use Ecto.Schema
  import Ecto.Changeset
  #import Ecto.Query


  schema "observations" do
    field :wallet_id, :integer
    field :stream_id, :integer
    field :target_id, :integer
    field :value, :string
    timestamps()
  end

  def changeset(observation, attrs) do
    required_fields = [:wallet_id, :stream_id, :target_id, :value]

    observation
    |> cast(attrs, required_fields)
    |> validate_required(required_fields)
  end



end
