defmodule Satori.WalletAuth do
  @moduledoc """
  Satori.WalletAuth represents a process whereby the client
  authenticates through signature verification.

  Upon connection the client will provide it's wallet public key,
  a message that it signed which is the current datetime, which
  must be within 5 seconds of what the server thinks is now, and a
  signature the server will then verify the signature and if it is
  valid, authenticate the client (not sure exactly what that means).
  """
  use Timex
  use DateTime

  def initialConnection(message, signature, pubkey) do
    if messageIsRecent(message) do
      case System.cmd("satori", ["verify", message, signature, pubkey]) do
        {"True\r\n", 0} -> authenticate(pubkey)
      end
    end
    # otherwise ignore them?
  end

  @doc """
  message should look like this: "2022-08-01 17:28:44.748691"
  """
  def messageIsRecent(message, ago \\ -5) do
    {:ok, compare} = Timex.parse(message, "%Y-%m-%d %H:%M:%S.%f", :strftime)
    messageTime = DateTime.from_naive!(compare, "Etc/UTC")
    {:gt, :gt} == {DateTime.compare(Timex.now(), messageTime), DateTime.compare(messageTime, Timex.shift(Timex.now(), seconds: ago))}
  end

  def authenticate(pubkey) do
    # I don't know what to do here - give them a session? connection? idk.
    # but now the client should be able to do stuff without having to prove it's identity with each request.
  end
end
