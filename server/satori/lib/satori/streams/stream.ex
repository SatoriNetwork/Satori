defmodule Satori.Streams.Stream do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Subscriber.Subscriber
  alias Satori.Wallet.Wallet
  alias Satori.Observation.Observation

  schema "streams" do
    field :cadence, :string
    field :name, :string
    field :sanctioned, :boolean, default: false
    field :source_name, :string
    #field :wallet_id, :integer

    has_many :subscriber, Subscriber
    has_many :observation, Observation
    belongs_to :wallet, Wallet

    timestamps()
  end

  @doc false
  def changeset(stream, attrs) do
    stream
    |> cast(attrs, [:wallet_id, :source_name, :name, :cadence, :sanctioned])
    |> validate_required([:wallet_id, :source_name, :name, :cadence, :sanctioned])
  end
end
