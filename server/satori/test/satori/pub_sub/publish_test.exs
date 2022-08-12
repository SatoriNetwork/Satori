defmodule Satori.PubSub.PublishTest do
  use Satori.DataCase
  import Mox

  alias Satori.PubSub.Publish
  alias Publish.{Input, Output, PublisherMock}

  setup :verify_on_exit!

  describe "publish/1" do
    @mock_topic "test topic"
    @mock_observation %{"some" => "test", "data" => "here"}

    @mock_input %Input{topic: @mock_topic, observation: @mock_observation}

    @publisher_return :ok

    test "calls Publisher.publish/2 with topic and observation from %Input{}" do
      PublisherMock
      |> expect(:publish, fn received_topic, received_observation ->
        assert @mock_topic == received_topic
        assert @mock_observation == received_observation

        @publisher_return
      end)

      Publish.publish(@mock_input)
    end

    test "returns %Output{} with nil error" do
      PublisherMock
      |> expect(:publish, fn _, _ ->
        @publisher_return
      end)

      assert %Output{error: nil} == Publish.publish(@mock_input)
    end
  end
end
