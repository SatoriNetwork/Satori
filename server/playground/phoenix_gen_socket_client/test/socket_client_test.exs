defmodule Phoenix.Channels.GenSocketClientTest do
  use ExUnit.Case, async: false

  alias TestSite.Endpoint
  alias Phoenix.Channels.GenSocketClient.TestSocket

  setup_all do
    ExUnit.CaptureLog.capture_log(fn -> Endpoint.start_link() end)
    :ok
  end

  setup do
    TestSite.Channel.subscribe()
    :ok
  end

  test "connection success" do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", %{}}} == TestSocket.join(socket, "channel:1")
  end

  test "no auto connect" do
    assert {:ok, socket} = start_socket(url(), query_params(), false)
    refute :connected == TestSocket.wait_connect_status(socket, 100)
    TestSocket.connect(socket)
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", %{}}} == TestSocket.join(socket, "channel:1")
  end

  test "connect with url and query_params" do
    # start the socket. false means do not connect for now.
    assert {:ok, socket} = start_socket(url(), query_params(), false)
    refute :connected == TestSocket.wait_connect_status(socket, 100)
    # connect by explicitly setting the url and query_params.
    TestSocket.connect(socket, url_updated(), query_params_updated())
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", %{}}} == TestSocket.join(socket, "channel:1")
  end

  test "client message push" do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", %{}}} == TestSocket.join(socket, "channel:1", %{"foo" => "bar"})
    assert {:ok, _ref} = TestSocket.push(socket, "channel:1", "some_event", %{"foo" => "bar"})
    assert_receive {TestSite.Channel, {:handle_in, "some_event", %{"foo" => "bar"}}}
  end

  test "send and response" do
    conn = join_channel()

    {:ok, payload} =
      TestSocket.push_sync(conn.socket, "channel:1", "sync_event", %{"foo" => "bar"})

    assert %{"status" => "ok", "response" => %{"foo" => "bar"}} = payload
  end

  test "sending a mesasge that cannot be encoded" do
    conn = join_channel()

    assert {:error,
            {:encoding_error, %Jason.EncodeError{message: "invalid byte 0xA6 in <<166>>"}}} =
             TestSocket.push_sync(conn.socket, "channel:1", "sync_event", %{
               "foo" => _invalid_string = <<166>>
             })
  end

  test "client message receive" do
    conn = join_channel()
    send(conn.server_channel, {:push, "some_event", %{"foo" => "bar"}})

    assert {:ok, {"channel:1", "some_event", %{"foo" => "bar"}}} =
             TestSocket.await_message(conn.socket)
  end

  test "leave the channel" do
    conn = join_channel()
    assert {:ok, %{}} == TestSocket.leave(conn.socket, "channel:1")
    assert_receive {TestSite.Channel, {:terminate, {:shutdown, :left}}}
  end

  test "push references are strings" do
    conn = join_channel()
    {:ok, ref} = TestSocket.push(conn.socket, "channel:1", "event")
    assert is_binary(ref)
  end

  test "push references are monotonically increasing on the same channel" do
    conn = join_channel()
    {:ok, ref1} = TestSocket.push(conn.socket, "channel:1", "event1")
    {:ok, ref2} = TestSocket.push(conn.socket, "channel:1", "event2")

    assert ref1 < ref2
  end

  test "push references are monotonically increasing on multiple channels" do
    conn = join_channel()
    {:ok, _} = TestSocket.join(conn.socket, "channel:2")
    {:ok, ref1} = TestSocket.push(conn.socket, "channel:1", "event1")
    {:ok, ref2} = TestSocket.push(conn.socket, "channel:2", "event2")

    assert ref1 < ref2
  end

  test "push references are monotonically increasing after leave/rejoin" do
    conn = join_channel()
    {:ok, ref1} = TestSocket.push(conn.socket, "channel:1", "event1")
    {:ok, %{}} = TestSocket.leave(conn.socket, "channel:1")
    TestSocket.join(conn.socket, "channel:1")
    {:ok, ref2} = TestSocket.push(conn.socket, "channel:1", "event2")

    assert ref1 < ref2
  end

  test "connection error" do
    assert {:ok, socket} = start_socket("ws://127.0.0.1:29877")
    assert {:disconnected, :econnrefused} == TestSocket.wait_connect_status(socket)
  end

  test "connection refused by socket" do
    assert {:ok, socket} = start_socket(url(), shared_secret: "invalid_secret")
    assert {:disconnected, {403, "Forbidden"}} == TestSocket.wait_connect_status(socket)
  end

  test "transport process terminates" do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    transport_pid = :sys.get_state(socket).transport_pid
    GenServer.stop(transport_pid)
    assert {:disconnected, {:transport_down, :normal}} == TestSocket.wait_connect_status(socket)

    # verify that we can reconnect and use the socket
    TestSocket.connect(socket)
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", _}} = TestSocket.join(socket, "channel:1")
  end

  test "can't interact when disconnected" do
    assert {:ok, socket} = start_socket()
    transport_pid = :sys.get_state(socket).transport_pid
    GenServer.stop(transport_pid)
    assert {:disconnected, _} = TestSocket.wait_connect_status(socket)
    assert {:error, :disconnected} = TestSocket.join(socket, "channel:1")
    assert {:error, :disconnected} = TestSocket.leave(socket, "channel:1")
    assert {:error, :disconnected} = TestSocket.push(socket, "channel:1", "some_event")
    assert {:error, :disconnected} = TestSocket.push_sync(socket, "channel:1", "some_event")
  end

  test "refused channel join" do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:error, reason} = TestSocket.join(socket, "invalid_channel")
    assert {:server_rejected, "invalid_channel", %{"reason" => "unmatched topic"}} == reason
  end

  test "double join" do
    conn = join_channel()
    TestSocket.join(conn.socket, "channel:1")
    assert {:error, :already_joined} == TestSocket.join(conn.socket, "channel:1")
  end

  test "no push before join" do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:error, :not_joined} == TestSocket.push(socket, "channel:1", "some_event")

    # Verify that we can still join after the invalid push
    assert {:ok, {"channel:1", _}} = TestSocket.join(socket, "channel:1")
    assert {:ok, _} = TestSocket.push(socket, "channel:1", "some_event")
  end

  test "server channel disconnects" do
    conn = join_channel()
    socket = conn.socket
    send(conn.server_channel, {:stop, :shutdown})
    assert_receive {^socket, :channel_closed, "channel:1", %{}}
  end

  test "server channel crashes" do
    conn = join_channel()
    socket = conn.socket

    ExUnit.CaptureLog.capture_log(fn ->
      send(conn.server_channel, {:crash, :some_reason})
      assert_receive {^socket, :channel_closed, "channel:1", %{}}
    end)
  end

  test "get status of joined channel" do
    conn = join_channel()
    assert TestSocket.joined?(conn.socket, "channel:1") == true
  end

  test "get status of not joined channel" do
    conn = join_channel()
    assert TestSocket.joined?(conn.socket, "channel:2") == false
  end

  defp join_channel do
    assert {:ok, socket} = start_socket()
    assert :connected == TestSocket.wait_connect_status(socket)
    assert {:ok, {"channel:1", %{}}} == TestSocket.join(socket, "channel:1")
    assert_receive {TestSite.Channel, {:join, "channel:1", _, server_channel}}

    %{socket: socket, server_channel: server_channel}
  end

  defp start_socket(url \\ url(), query_params \\ query_params(), connect \\ true) do
    TestSocket.start_link(
      Phoenix.Channels.GenSocketClient.Transport.WebSocketClient,
      url,
      query_params,
      connect
    )
  end

  defp url() do
    "#{Endpoint.url()}/test_socket/websocket"
    |> String.replace(~r(http://), "ws://")
    |> String.replace(~r(https://), "wss://")
  end

  defp query_params(), do: [{"shared_secret", "supersecret"}]

  defp url_updated() do
    "#{Endpoint.url()}/test_socket_updated/websocket"
    |> String.replace(~r(http://), "ws://")
    |> String.replace(~r(https://), "wss://")
  end

  defp query_params_updated(), do: [{"shared_secret", "supersecret_updated"}]
end
