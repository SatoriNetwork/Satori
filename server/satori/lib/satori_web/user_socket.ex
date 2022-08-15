defmodule SatoriWeb.UserSocket do
  use Phoenix.Socket

  use Absinthe.Phoenix.Socket,
    schema: SatoriWeb.GraphQL.Schema

  @impl true
  def connect(params, socket) do
    if authorized?(params) do
      {:ok, socket}
    else
      :error
    end
  end

  @impl true
  def id(_socket), do: nil

  defp authorized?(%{"token" => token}) do
    case SatoriWeb.GraphQL.AuthToken.verify(token) do
      {:ok, _} -> true
      _ -> false
    end
  end

  defp authorized?(_), do: false
end
