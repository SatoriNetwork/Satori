defmodule Satori.Streams.Stream do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Subscribers.Subscriber
  alias Satori.Wallets.Wallet
  alias Satori.Observations.Observation

  @fields ~w(wallet_id source_name name cadence sanctioned prediction_of)a
  @required ~w(wallet_id source_name name)a

  schema "streams" do
    field :cadence, :string
    field :name, :string
    field :sanctioned, :boolean, default: false
    field :source_name, :string
    # This is the ID of the stream that this stream predicts,
    # if null this is a primary raw data stream,
    # if not null this is a prediction stream
    field :prediction_of, :integer # is a stream.id
    # has_one :stream, __MODULE__, foreign_key: :prediction_of

    has_many :subscriber, Subscriber
    has_many :observation, Observation
    belongs_to :wallet, Wallet

    timestamps()
  end

  @doc false
  def changeset(stream, attrs) do
    stream
    |> cast(attrs, @fields)
    |> validate_required(@required)
  end
end
