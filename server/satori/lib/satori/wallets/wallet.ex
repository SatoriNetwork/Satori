defmodule Satori.Wallets.Wallet do
  use Ecto.Schema
  import Ecto.Changeset
  #alias Satori.Accounts.User
  alias Satori.Devices.Device
  alias Satori.Streams.Stream

  #@fields ~w(user_id address pubkey)a
  @fields ~w(address pubkey)a
  @required ~w(address pubkey)a

  schema "wallets" do
    field :address, :string
    field :pubkey, :string

    #belongs_to :user, User
    has_one :devices, Device
    has_many :stream, Stream

    timestamps()
  end

  @doc false
  def changeset(wallet, attrs) do
    wallet
    |> cast(attrs, @fields)
    |> validate_required(@required)
  end
end
