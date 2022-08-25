defmodule GraphqlPubsub.Repo do
  use Ecto.Repo,
    otp_app: :graphql_pubsub,
    adapter: Ecto.Adapters.Postgres
end
