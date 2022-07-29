defmodule Satori.WalletAuth do
  @moduledoc """
  Satori.WalletAuth represents a process whereby the client
  authenticates through signature verification.

  Upon connection the client will provide it's wallet address
  (a version of it's public key), the server will generate a
  random string, send it to the client, and the client will
  respond with a signature which the server will verify.
  https://elixirforum.com/t/right-way-to-use-crypto-verify/19014
  https://github.com/ntrepid8/ex_crypto
  https://hexdocs.pm/web3x/0.6.3/Web3x.Wallet.html#verify_message?/4 eth
  https://blog.lelonek.me/how-to-calculate-bitcoin-address-in-elixir-68939af4f0e9
  https://hexdocs.pm/curvy/Curvy.html
  """
  def index() do
    # ExPublicKey.verify(message, signature, rsa_public_key)
    #or
    #message = "whatever"
    #signature_base64 = "zFuf7bRH4RHwyktaqHQwmX5rn3LfSb4dKo..." # truncated
    #signature = Base.decode64!(signature_base64)
    #:crypto.verify(:rsa, :sha256, message, signature, public_key)
    # actually I think this is best
    #:crypto.verify(
    #  :ecdsa,
    #  :sha256,
    #  "message",
    #  signature,
    #  [public_key, :secp256k1]
    #)
  end
end
