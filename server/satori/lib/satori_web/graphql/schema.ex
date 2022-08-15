defmodule SatoriWeb.GraphQL.Schema do
  use Absinthe.Schema

  alias Satori.PubSub.Subscribe

  object :test do
    field :id, :id
  end

  object :observation do
    field :id, :id
    field :stream_id, :id
    field :target_id, :id

    field :value, :string
  end

  query do
    @desc "Test query"
    field :test, :test do
      resolve(fn _, _, _ ->
        {:ok, %{id: Ecto.UUID.generate()}}
      end)
    end
  end

  subscription do
    field :test_sub, :test do
      config(fn _, _ ->
        {:ok, topic: "test"}
      end)
    end

    field :observations, :observation do
      arg(:topic, non_null(:string))

      config(fn args, _ ->
        output =
          %Subscribe.Input{
            topic: args.topic
          }
          |> Subscribe.subscribe()

        if output.error == nil do
          {:ok, topic: args.topic}
        else
          {:error, output.error}
        end
      end)
    end
  end
end
