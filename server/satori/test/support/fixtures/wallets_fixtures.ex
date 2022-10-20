defmodule Satori.WalletsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Satori.Wallets` context.
  """

  @doc """
  Generate a wallet.
  """
  def wallet_fixture(attrs \\ %{}) do
    {:ok, wallet} =
      attrs
      |> Enum.into(%{
        address: "some address",
        pubkey: "some pubkey",
        user_id: 42
      })
      |> Satori.Wallets.create_wallet()

    wallet
  end
end
