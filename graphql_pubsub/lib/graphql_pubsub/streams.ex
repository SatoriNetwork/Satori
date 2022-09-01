defmodule GraphqlPubsub.Streams do

  import Ecto.Query, warn: false
  alias GraphqlPubsub.Repo

  alias GraphqlPubsub.Streams.{Observation, TargetSubscription}
  # alias GraphqlPubsub.Accounts.User

  require Logger

  def list_observations do
    Repo.all(Observation)
  end

  def create_observation(attrs) do
    %Observation{}
    |> Observation.changeset(attrs)
    |> Repo.insert()
  end


  def get_subscription(attrs) do
    Repo.one from p in TargetSubscription, where: p.device_id == ^attrs.device_id and p.stream_id == ^attrs.stream_id and p.target_id == ^attrs.target_id
    # Repo.get_by!(TargetSubscription, device_id: attrs.device_id, stream_id: attrs.stream_id, target_id: attrs.target_id)
    # Repo.get_by!(TargetSubscription, device_id: attrs.device_id).first
  end


  # @spec find_or_create_subscription(attrs) :: {:ok, TargetSubscription} | {:error, String}
  def find_or_create_subscription(attrs) do
    case get_subscription(attrs) do
      subscription ->
        case subscription do
          nil -> create_subscription(attrs)
          _ -> {:ok, subscription}
        end
    end
  end


  def create_subscription(attrs) do
    %TargetSubscription{}
    |> TargetSubscription.changeset(attrs)
    |> Repo.insert()
  end


  @spec list_subscription(any) :: any
  def list_subscription(criteria) do
    query = from p in TargetSubscription

    Enum.reduce(criteria, query, fn
      {:limit, limit}, query ->
        from p in query, limit: ^limit

      {:order, order}, query ->
        from p in query, order_by: [{^order, :id}]

      {:device_id, device_id}, query ->
        from q in query, where: q.device_id == ^device_id

    end)
    |> Repo.all
  end


  defp filter_with(filters, query) do
    Enum.reduce(filters, query, fn
      {:matching, term}, query ->
        pattern = "%#{term}%"

        from q in query,
        where:
          ilike(q.device_id, ^pattern)

      # {:device_id, value}, query ->
      #   from q in query, where: q.device_id == ^value

    end)
  end


end
