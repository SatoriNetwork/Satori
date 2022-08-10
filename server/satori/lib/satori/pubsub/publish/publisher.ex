defmodule Satori.PubSub.Publish.Publisher do
  @callback publish(topic :: binary(), observation :: map()) :: :ok, {:error, reason :: atom()}
  def publish(topic, observation) do
    impl().publish(topic, observation)
  end

  defp impl do
    Application.get_env(:satori, __MODULE__)
  end
end
