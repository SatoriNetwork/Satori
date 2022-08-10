defmodule SatoriWeb.GraphQL.Schema do
  use Absinthe.Schema

  object :test do
    field :id, :id
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
      config fn _, _ ->
        {:ok, topic: "test"}
      end
    end
  end
end
