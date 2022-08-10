defmodule Satori.Wallets.Wallet do
  use Ecto.Schema
  import Ecto.Changeset
  alias Satori.Accounts.User
  alias Satori.Devices.Device
  alias Satori.Streams.Stream

  @fields ~w(user_id address script_hash)a
  @required ~w(address)a

  schema "wallets" do
    field(:address, :string)
    field(:script_hash, :string)

    belongs_to(:user, User)
    has_many(:devices, Device)
    has_many(:stream, Stream)

    timestamps()
  end

  @doc false
  def changeset(wallet, attrs) do
    wallet
    |> cast(attrs, @fields)
    |> validate_required(@required)
  end
end
