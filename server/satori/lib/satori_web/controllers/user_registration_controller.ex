defmodule SatoriWeb.UserRegistrationController do
  use SatoriWeb, :controller

  alias Satori.Accounts
  alias Satori.Accounts.User
  alias SatoriWeb.UserAuth

  def new(conn, _params) do
    changeset = Accounts.change_user_registration(%User{})
    render(conn, "new.html", changeset: changeset)
  end

  def wallet(conn, _params) do
    changeset = Accounts.change_user_registration(%User{})
    render(conn, "wallet.html", changeset: changeset)
  end

  def create(conn, %{"user" => user_params}) do
    case Accounts.register_user(user_params) do
      {:ok, user} ->
        {:ok, _} =
          Accounts.deliver_user_confirmation_instructions(
            user,
            &Routes.user_confirmation_url(conn, :edit, &1)
          )

        conn
        |> put_flash(:info, "User created successfully.")
        |> UserAuth.log_in_user(user)

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end

  def create_with_wallet(conn, %{"user" => %{"public_key" => public_key} = user_params}) do
    IO.inspect(user_params)

    case Accounts.register_user(%{
           "email" => String.replace(public_key, " ", "") <> "@test.com",
           "password" => "123456789abc",
           "public_key" => public_key
         }) do
      {:ok, user} ->
        # {:ok, _} =
        #   Accounts.deliver_user_confirmation_instructions(
        #     user,
        #     &Routes.user_confirmation_url(conn, :edit, &1)
        #   )

        conn
        |> put_flash(:info, "User created successfully.")
        |> UserAuth.log_in_user(user)

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end
end
