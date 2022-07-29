defmodule Satori.StreamFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Satori.Stream` context.
  """

  @doc """
  Generate a observation.
  """
  def observation_fixture(attrs \\ %{}) do
    {:ok, observation} =
      attrs
      |> Enum.into(%{
        source_id: 42,
        stream_id: 42,
        target_id: 42,
        value: "some value",
        wallet_id: 42
      })
      |> Satori.Stream.create_observation()

    observation
  end
end
