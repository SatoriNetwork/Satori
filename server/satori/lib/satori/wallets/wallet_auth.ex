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
  # use DateTime

  def initialConnection(message, signature, pubkey) do
    if messageIsRecent(message) do
      ## work around solution:
      # case System.cmd("satori", ["verify", message, signature, pubkey]) do
      #  {"True\r\n", 0} -> authenticate(pubkey)
      # end
      case Satori.Wallets.Signature.verify!(message, signature, pubkey) do
        true -> authenticate(pubkey)
        # otherwise ignore them?
        false -> false
      end
    end
  end

  @doc """
  message should look like this: "2022-08-01 17:28:44.748691"
  """
  def messageIsRecent(message, ago \\ -5) do
    {:ok, compare} = Timex.parse(message, "%Y-%m-%d %H:%M:%S.%f", :strftime)
    messageTime = DateTime.from_naive!(compare, "Etc/UTC")

    {:gt, :gt} ==
      {DateTime.compare(Timex.now(), messageTime),
       DateTime.compare(messageTime, Timex.shift(Timex.now(), seconds: ago))}
  end

  def authenticate(pubkey) do
    pubkey
    # Sign to create `token` when first create account/login
    # token = Phoenix.Token.sign(SatoriWeb.Endpoint, salt, pubkey)
    # Store the {session, token}

    # Maybe timer for {session, token}

    # Session is generated when ever client connect to server

    # At the next login
    # Fetch `token` by pubkey from DB by `session`
    # If `token` found --> verify token
    # case Phoenix.Token.verify(SatoriWeb.Endpoint, salt, token) do
    #   {:ok, pubkey} ->
    #     # Do something with return pubkey
    #     {:ok, assign(socket, :pubkey, pubkey)}

    #   {:error, _error} ->
    #     # Error case ->> re-login
    #     {:ok, socket}
    # end

    # `token` not found (expired) --> re-login
  end
end
