defmodule Satori.Targets.Target do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Subscriber.Subscriber
  alias Satori.Observation.Observation

  schema "targets" do
    field :name, :string

    has_many :subscriber, Subscriber
    has_many :observation, Observation

    timestamps()
  end

  @doc false
  def changeset(target, attrs) do
    target
    |> cast(attrs, [:name])
    |> validate_required([:name])
  end
end
