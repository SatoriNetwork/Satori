defmodule Satori.Observations.Observation do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Stream.Stream
  alias Satori.Target.Target
  alias Satori.Wallet.Wallet

  schema "observations" do
    #field :stream_id, :integer
    #field :target_id, :integer
    field :value, :string
    ## even though stream names are not unique,
    ## the stream knows what wallet it belongs to,
    ## making the combination unique.
    ## So if we include this it's merely for an
    ## optimization for efficient querying:
    #field :wallet_id, :integer

    belongs_to :stream, Stream
    belongs_to :wallet, Wallet
    belongs_to :target, Target

    timestamps()
  end

  @doc false
  def changeset(observation, attrs) do
    observation
    |> cast(attrs, [:stream_id, :wallet_id, :target_id, :value])
    |> validate_required([:stream_id, :wallet_id, :target_id, :value])
  end
end
