defmodule GraphqlPubsub.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Ecto repository
      GraphqlPubsub.Repo,
      # Start the Telemetry supervisor
      GraphqlPubsubWeb.Telemetry,
      # Start the Endpoint (http/https)
      GraphqlPubsubWeb.Endpoint,

      # Start the PubSub system
      {Phoenix.PubSub, [name: GraphqlPubsub.PubSub, adapter: Phoenix.PubSub.PG2]}

      # {Absinthe.Subscription, GraphqlPubsubWeb.Endpoint}

      # Start a worker by calling: GraphqlPubsub.Worker.start_link(arg)
      # {GraphqlPubsub.Worker, arg}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: GraphqlPubsub.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    GraphqlPubsubWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
