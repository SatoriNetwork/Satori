defmodule GraphqlPubsub.Streams.TargetSubscription do
  use Ecto.Schema
  import Ecto.Changeset

  schema "subscribers" do
    field :stream_id, :integer
    field :device_id, :integer
    field :target_id, :integer
    timestamps()
  end


  def changeset(target_subscription, attrs) do
    required_fields = [:stream_id, :device_id, :target_id]

    target_subscription
    |> cast(attrs, required_fields)
    |> validate_required(required_fields)
  end



end
