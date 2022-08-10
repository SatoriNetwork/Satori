defmodule SatoriWeb.WalletRegistrationController do
  use SatoriWeb, :controller

  alias Satori.Wallets
  alias Satori.Wallets.Wallet
  alias SatoriWeb.WalletAuth
  # alias Satori.Wallets.Signature
  # alias SatoriWeb.UserAuth

  def new(conn, _params) do
    # changeset = Accounts.change_user_registration(%User{})

    render(conn, "new.html", changeset: Wallets.change_wallet(%Wallet{}))
  end

  def create(conn, %{
        "wallet" =>
          %{"message" => message, "signature" => signature, "address" => pubkey} = _user_params
      }) do
    ## verify wallet here
    # case Signature.verify!(message, signature, pubkey) do
    case verify!(message, signature, pubkey) do
      true ->
        case Wallets.create_wallet(%{"address" => pubkey}) do
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

  defp verify!(_message, _signature, _pubkey) do
    true
  end
end
