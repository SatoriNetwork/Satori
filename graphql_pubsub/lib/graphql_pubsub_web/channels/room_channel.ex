defmodule GraphqlPubsubWeb.RoomChannel do
  use GraphqlPubsubWeb, :channel

  @impl true
  def join("sat:*", payload, socket) do
    {:ok, socket}



    # if authorized?(payload) do
    #   {:ok, socket}
    # else
    #   {:error, %{reason: "unauthorized"}}
    # end
  end


  def join("stream:" <> _private_room_id, _params, socket) do
    {:ok, socket}
  end


  # Just replies with exact same payload
  @impl true
  def handle_in("echo", payload, socket) do
    {:reply, {:ok, payload}, socket}
  end


  # def handle_in("UPDATE", %{"body" => body}, socket) do
  #   broadcast!(socket, "UPDATE", %{body: body})
  #   {:noreply, socket}
  # end

  # Channels can be used in a request/response fashion
  # by sending replies to requests from the client
  @impl true
  def handle_in("UPDATE", payload, socket) do
    {:reply, {:ok, payload}, socket}
  end

  # It is also common to receive messages from the client and
  # broadcast to everyone in the current topic (room:lobby).
  @impl true
  def handle_in("shout", payload, socket) do
    broadcast(socket, "shout", payload)
    {:noreply, socket}
  end

  # Add authorization logic here as required.
  defp authorized?(_payload) do
    true
  end
end
