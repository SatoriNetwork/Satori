defmodule SatoriWeb.Resolvers.Device do
  alias Satori.Devices
  # alias SatoriWeb.Schema.ChangesetErrors

  def device(_, %{id: id}, _) do
    {:ok, Devices.get_device!(id)}
  end

  def devices(_, args, _) do
    {:ok, Devices.list_devices(args)}
  end

  def wallet_for_device(device, _, _) do
    {:ok, Devices.wallet_for_device(device)}
  end
end
