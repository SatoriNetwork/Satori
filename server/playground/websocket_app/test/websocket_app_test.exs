defmodule WebsocketAppTest do
  use ExUnit.Case
  doctest WebsocketApp

  test "greets the world" do
    assert WebsocketApp.hello() == :world
  end
end
