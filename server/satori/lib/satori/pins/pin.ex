defmodule Satori.Pins.Pin do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Stream.Stream
  alias Satori.Target.Target
  alias Satori.Wallet.Wallet

  @fields ~w(wallet_id stream_id target_id ipns)a
  @required ~w(wallet_id stream_id target_id ipns)a

  schema "pins" do
    field :ipns, :string

    belongs_to :stream, Stream
    belongs_to :wallet, Wallet
    belongs_to :target, Target

    timestamps()
  end

  @doc false
  def changeset(pin, attrs) do
    pin
    |> cast(attrs, @fields)
    |> validate_required(@required)
  end
end
