defmodule Satori.Wallets do
  @moduledoc """
  The Wallets context.
  """

  import Ecto.Query, warn: false
  alias Satori.Repo

  alias Satori.Wallets.{Wallet, WalletToken}
  alias Satori.Devices.Device

  @doc """
  Returns the list of wallets.

  ## Examples

      iex> list_wallets()
      [%Wallet{}, ...]

  """
  def list_wallets do
    Repo.all(Wallet)
  end

@doc """
  Returns the list of Wallets matching the `criteria`.

  Examples Criteria

    [{:limit, 15}, {:order, :asc}, {:filter, [{:matching, "california"}, {:public_key, abce123}]}]

  """

  def list_wallets(criteria) do
    query = from w in Wallet

    Enum.reduce(criteria, query, fn
      {:limit, limit}, query ->
        from w in query, limit: ^limit

        {:filter, filters}, query ->
          filter_with(filters, query)

        # {:order, order}, query ->
        #   from w in query, order_by [{^order, :id}]
      end)
      |> IO.inspect()
      |> Repo.all
      |> Repo.preload(:device)
  end

  defp filter_with(filters, query) do
    Enum.reduce(filters, query, fn
      {:matching, term}, query ->
        pattern = "%#{term}%"

        from w in query,
          where:
            ilike(w.address, ^pattern) or
              ilike(w.public_key, ^pattern)

        {:address, value}, query ->
          from w in query, where: w.address == ^value

        {:public_key, value}, query ->
          from w in query, where: w.public_key == ^value
    end)
  end

  def device_for_wallet(%Wallet{} = wallet) do
    Device
    |> where(wallet_id: ^wallet.id)
    |> Repo.all
  end

  @doc """
  Gets a single wallet.

  Raises `Ecto.NoResultsError` if the Wallet does not exist.

  ## Examples

      iex> get_wallet!(123)
      %Wallet{}

      iex> get_wallet!(456)
      ** (Ecto.NoResultsError)

  """
  def get_wallet!(id) do
    Repo.get!(Wallet, id)
   |> Repo.preload(:device)
  end

  @doc """
  Creates a wallet.

  ## Examples

      iex> create_wallet(%{field: value})
      {:ok, %Wallet{}}

      iex> create_wallet(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_wallet(attrs \\ %{}) do
    %Wallet{}
    |> Wallet.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a wallet.

  ## Examples

      iex> update_wallet(wallet, %{field: new_value})
      {:ok, %Wallet{}}

      iex> update_wallet(wallet, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_wallet(%Wallet{} = wallet, attrs) do
    wallet
    |> Wallet.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a wallet.

  ## Examples

      iex> delete_wallet(wallet)
      {:ok, %Wallet{}}

      iex> delete_wallet(wallet)
      {:error, %Ecto.Changeset{}}

  """
  def delete_wallet(%Wallet{} = wallet) do
    Repo.delete(wallet)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking wallet changes.

  ## Examples

      iex> change_wallet(wallet)
      %Ecto.Changeset{data: %Wallet{}}

  """
  def change_wallet(%Wallet{} = wallet, attrs \\ %{}) do
    Wallet.changeset(wallet, attrs)
  end

  ## Session

  @doc """
  Generates a session token.
  """
  def generate_wallet_session_token(wallet) do
    {token, wallet_token} = WalletToken.build_session_token(wallet)
    Repo.insert!(wallet_token)
    token
  end

  def get_wallet_by_session_token(token) do
    {:ok, query} = WalletToken.verify_session_token_query(token)
    Repo.one(query)
  end

  def get_wallet_by_address(address)
      when is_binary(address) do
    Repo.get_by(Wallet, address: address)
  end

  def delete_session_token(token) do
    Repo.delete_all(WalletToken.token_and_context_query(token, "session"))
    :ok
  end

  #############################################################################
  # Data Loader Functions
  #############################################################################

end
