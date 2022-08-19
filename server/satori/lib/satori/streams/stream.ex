defmodule Satori.Streams.Stream do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Subscriber.Subscriber
  alias Satori.Wallet.Wallet
  alias Satori.Observation.Observation

  @fields ~w(wallet_id source_name name cadence sanctioned stream_id)a
  @required ~w(wallet_id source_name name)a


  schema "streams" do
    field :cadence, :string
    field :name, :string
    field :sanctioned, :boolean, default: false
    field :source_name, :string
    # This is the ID of the stream that this stream predicts,
    # if null this is a primary raw data stream,
    # if not null this is a prediction stream
    field :stream_id, :integer
    #has_one :stream, __MODULE__, foreign_key: :stream_id

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
