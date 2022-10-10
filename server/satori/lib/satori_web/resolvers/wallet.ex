defmodule SatoriWeb.Resolvers.Wallet do
  alias Satori.Wallets
  # alias SatoriWeb.Schema.ChangesetErrors

  def wallet(_, %{id: id}, _) do
    {:ok, Wallets.get_wallet!(id)}
  end

  def wallets(_, args, _) do
    {:ok, Wallets.list_wallets(args)}
  end

  def device_for_wallet(wallet, _, _) do
    {:ok, Wallets.device_for_wallet(wallet)}
  end
end
