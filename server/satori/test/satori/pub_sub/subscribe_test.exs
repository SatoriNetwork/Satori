defmodule Satori.PubSub.SubscribeTest do
  use Satori.DataCase
  import Mox

  alias Satori.PubSub.Subscribe
  alias Subscribe.{Input, Output}

  setup :verify_on_exit!

  @mock_topic "test topic"

  @mock_input %Input{topic: @mock_topic}

  describe "subscribe/1" do
    @tag :current
    test "returns %Output{} with nil error" do
      assert %Output{error: nil} == Subscribe.subscribe(@mock_input)
    end
  end
end
