defmodule Phoenix.GenSocketClient.Mixfile do
  use Mix.Project

  @version "4.1.0"
  @github_url "https://github.com/J0/phoenix_gen_socket_client"

  def project do
    [
      app: :phoenix_gen_socket_client,
      version: @version,
      elixir: "~> 1.8",
      elixirc_paths: elixirc_paths(Mix.env()),
      build_embedded: Mix.env() == :prod,
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      package: package(),
      description: "Socket client behaviour for phoenix channels.",
      docs: [
        source_url: @github_url,
        source_ref: "v#{@version}",
        main: "readme",
        extras: ["README.md"]
      ]
    ]
  end

  def application do
    [extra_applications: [:logger | extra_applications(Mix.env())]]
  end

  defp extra_applications(:prod), do: []
  defp extra_applications(_), do: [:websocket_client]

  defp deps do
    [
      {:websocket_client, "~> 1.2", optional: true},
      {:jason, "~> 1.1", optional: true},
      {:phoenix, "~> 1.3", only: :test},
      {:cowboy, "~> 1.0", only: :test},
      {:credo, "~> 0.8.10", only: [:dev, :test], runtime: false},
      {:dialyze, "~> 0.2.1", only: :dev},
      {:ex_doc, "~> 0.22.1", only: :dev, runtime: false}
    ]
  end

  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  defp package do
    [
      maintainers: ["J0"],
      licenses: ["MIT"],
      links: %{
        "GitHub" => @github_url,
        "Docs" => "http://hexdocs.pm/phoenix_gen_socket_client"
      }
    ]
  end
end
