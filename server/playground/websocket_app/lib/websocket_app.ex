defmodule WebsocketApp do
  use Application

  def start(_type, _args) do
    children = [
      Plug.Cowboy.child_spec(
        scheme: :http,
        plug: WebsocketApp.Router,
        options: [
          dispatch: dispatch(),
          port: 4000
        ]
      ),
      Registry.child_spec(
        keys: :duplicate,
        name: Registry.WebsocketApp
      )
    ]

    opts = [strategy: :one_for_one, name: WebsocketApp.Application]
    Supervisor.start_link(children, opts)
  end

  defp dispatch do
    [
      {:_,
        [
          {"/ws/[...]", WebsocketApp.SocketHandler, []},
          {:_, Plug.Cowboy.Handler, {WebsocketApp.Router, []}}
        ]
      }
    ]
  end
end
