defmodule Satori.Devices do
  @moduledoc """
  The Devices context.
  """

  import Ecto.Query, warn: false
  alias Satori.Repo

  alias Satori.Devices.Device
  alias Satori.Wallets.Wallet

  @doc """
  Returns the list of devices.

  ## Examples

      iex> list_devices()
      [%Device{}, ...]

  """
  def list_devices do
    Repo.all(Device)
  end

  # def my_list_devices(criteria), do: list_devices(criteria) |> Repo.preload(:wallet)

  @doc """
  Returns the list of devices matching the `criteria`.

  Examples Criteria

    [{:limit, 15}, {:order, :asc}, {:filter, [{:matching, "macbook"}, {:ram, 6}]}]

  """

  def list_devices(criteria) do
    query = from d in Device

    Enum.reduce(criteria, query, fn
      {:limit, limit}, query ->
        from d in query, limit: ^limit

        {:filter, filters}, query ->
          filter_with(filters, query)

        # {:order, order}, query ->
        #   from d in query, order_by [{^order, :id}]
      end)
      |> IO.inspect()
      |> Repo.all
      |> Repo.preload(:wallet)
  end

  defp filter_with(filters, query) do
    Enum.reduce(filters, query, fn
      {:matching, term}, query ->
        pattern = "%#{term}%"

        from d in query,
          where:
            ilike(d.name, ^pattern) or
              ilike(d.cpu, ^pattern)

        {:bandwidth, value}, query ->
          from d in query, where: d.bandwidth == ^value

        {:disk, value}, query ->
          from d in query, where: d.disk == ^value

        {:ram, value}, query ->
          from d in query, where: d.ram == ^value
    end)
  end

  def wallet_for_device(%Device{} = device) do
    Wallet
    |> where(device_id: ^device.id)
    |> Repo.all
  end

  @doc """
  Gets a single device.

  Raises `Ecto.NoResultsError` if the Device does not exist.

  ## Examples

      iex> get_device!(123)
      %Device{}

      iex> get_device!(456)
      ** (Ecto.NoResultsError)

  """
  def get_device!(id) do
    Repo.get!(Device, id)
   |> Repo.preload(:wallet)
  end

  @doc """
  Creates a device.

  ## Examples

      iex> create_device(%{field: value})
      {:ok, %Device{}}

      iex> create_device(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_device(attrs \\ %{}) do
    %Device{}
    |> Device.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a device.

  ## Examples

      iex> update_device(device, %{field: new_value})
      {:ok, %Device{}}

      iex> update_device(device, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_device(%Device{} = device, attrs) do
    device
    |> Device.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a device.

  ## Examples

      iex> delete_device(device)
      {:ok, %Device{}}

      iex> delete_device(device)
      {:error, %Ecto.Changeset{}}

  """
  def delete_device(%Device{} = device) do
    Repo.delete(device)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking device changes.

  ## Examples

      iex> change_device(device)
      %Ecto.Changeset{data: %Device{}}

  """
  def change_device(%Device{} = device, attrs \\ %{}) do
    Device.changeset(device, attrs)
  end

  #############################################################################
  # Data Loader Functions
  #############################################################################

end
