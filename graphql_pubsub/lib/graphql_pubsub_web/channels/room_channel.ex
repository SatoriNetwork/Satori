defmodule GraphqlPubsubWeb.RoomChannel do
  use GraphqlPubsubWeb, :channel

  alias GraphqlPubsubWeb.Resolvers

  # @impl true
  # def join("sat:*", payload, socket) do
  #   {:ok, socket}



  #   # if authorized?(payload) do
  #   #   {:ok, socket}
  #   # else
  #   #   {:error, %{reason: "unauthorized"}}
  #   # end
  # end


  @impl true
  def join("stream:" <> _private_room_id, _params, socket) do
    {:ok, socket}
  end


  # Just replies with exact same payload
  @impl true
  def handle_in("echo", payload, socket) do
    {:reply, {:ok, payload}, socket}
  end


  # It is also common to receive messages from the client and
  # broadcast to everyone in the current topic (room:lobby).
  @impl true
  def handle_in("published_observation", payload, socket) do
    broadcast(socket, "published_observation", payload)
    # IO.puts(payload)
    Resolvers.Streams.create_client_observation(payload)
    {:noreply, socket}
  end

  # Add authorization logic here as required.
  defp authorized?(_payload) do
    true
  end
end
