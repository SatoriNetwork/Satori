defmodule Satori.PubSub.Publish.Topic do
  @spec maybe_create(binary()) :: :ok | {:error, atom()}
  def maybe_create(_topic) do
    :ok
  end
end
