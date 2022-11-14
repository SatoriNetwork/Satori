defmodule PubsubWebsocketTest do
  use ExUnit.Case
  doctest PubsubWebsocket

  test "greets the world" do
    assert PubsubWebsocket.hello() == :world
  end
end
