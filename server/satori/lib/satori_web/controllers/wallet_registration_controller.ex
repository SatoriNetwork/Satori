defmodule SatoriWeb.WalletRegistrationController do
  use SatoriWeb, :controller

  alias Satori.Wallets
  alias Satori.Wallets.Wallet
  alias SatoriWeb.WalletAuth
  alias Satori.Wallets.Signature
  # alias SatoriWeb.UserAuth

  def new(conn, _params) do
    # changeset = Accounts.change_user_registration(%User{})

    render(conn, "new.html", changeset: Wallets.change_wallet(%Wallet{}))
  end

  def create(conn, %{
        "wallet" =>
          %{"message" => message, "signature" => signature, "public_key" => public_key, "address" => address} = _user_params
      }) do
    case verify!(message, signature, public_key) do
      true ->
        case Wallets.create_wallet(%{"public_key" => public_key}) do
          {:ok, wallet} ->
            conn
            |> put_flash(:info, "Wallet created successfully.")
            |> WalletAuth.log_in_wallet(wallet)

          {:error, %Ecto.Changeset{} = changeset} ->
            render(conn, "new.html", changeset: changeset)
        end

      _ ->
        render(conn, "new.html", changeset: Wallets.change_wallet(%Wallet{}))
    end
  end

  defp verify!(_message, _signature, _public_key) do
    if messageIsRecent(_message) do
      Satori.Wallets.Signature.verify!(_message, _signature, _public_key)
    end
    false
  end

  defp messageIsRecent(_message, _ago \\ -5) do
    {:ok, _compare} = Timex.parse(_message, "%Y-%m-%d %H:%M:%S.%f", :strftime)
    _messageTime = DateTime.from_naive!(_compare, "Etc/UTC")

    {:gt, :gt} ==
      {DateTime.compare(Timex.now(), _messageTime),
       DateTime.compare(_messageTime, Timex.shift(Timex.now(), seconds: _ago))}
  end
end
