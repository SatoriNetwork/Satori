defmodule Satori.Subscribers.Subscriber do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Device.Device
  alias Satori.Stream.Stream
  alias Satori.Target.Target

  schema "subscribers" do
    #field :device_id, :integer
    #field :stream_id, :integer
    #field :target_id, :integer

    belongs_to :device, Device
    belongs_to :stream, Stream
    belongs_to :target, Target

    timestamps()
  end

  @doc false
  def changeset(subscriber, attrs) do
    subscriber
    |> cast(attrs, [:stream_id, :device_id, :target_id])
    |> validate_required([:stream_id, :device_id, :target_id])
  end
end
