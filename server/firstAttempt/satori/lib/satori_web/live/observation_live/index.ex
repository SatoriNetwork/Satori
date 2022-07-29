defmodule SatoriWeb.ObservationLive.Index do
  use SatoriWeb, :live_view

  alias Satori.Stream
  alias Satori.Stream.Observation

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :observation_collection, list_observation())}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :edit, %{"id" => id}) do
    socket
    |> assign(:page_title, "Edit Observation")
    |> assign(:observation, Stream.get_observation!(id))
  end

  defp apply_action(socket, :new, _params) do
    socket
    |> assign(:page_title, "New Observation")
    |> assign(:observation, %Observation{})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Observation")
    |> assign(:observation, nil)
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    observation = Stream.get_observation!(id)
    {:ok, _} = Stream.delete_observation(observation)

    {:noreply, assign(socket, :observation_collection, list_observation())}
  end

  defp list_observation do
    Stream.list_observation()
  end
end
