defmodule Satori.StreamTest do
  use Satori.DataCase

  alias Satori.Stream

  describe "observation" do
    alias Satori.Stream.Observation

    import Satori.StreamFixtures

    @invalid_attrs %{stream_id: nil, target_id: nil, value: nil, wallet_id: nil}

    test "list_observation/0 returns all observation" do
      observation = observation_fixture()
      assert Stream.list_observation() == [observation]
    end

    test "get_observation!/1 returns the observation with given id" do
      observation = observation_fixture()
      assert Stream.get_observation!(observation.id) == observation
    end

    test "create_observation/1 with valid data creates a observation" do
      valid_attrs = %{stream_id: 42, target_id: 42, value: "some value", wallet_id: 42}

      assert {:ok, %Observation{} = observation} = Stream.create_observation(valid_attrs)
      assert observation.stream_id == 42
      assert observation.target_id == 42
      assert observation.value == "some value"
      assert observation.wallet_id == 42
    end

    test "create_observation/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Stream.create_observation(@invalid_attrs)
    end

    test "update_observation/2 with valid data updates the observation" do
      observation = observation_fixture()
      update_attrs = %{stream_id: 43, target_id: 43, value: "some updated value", wallet_id: 43}

      assert {:ok, %Observation{} = observation} = Stream.update_observation(observation, update_attrs)
      assert observation.stream_id == 43
      assert observation.target_id == 43
      assert observation.value == "some updated value"
      assert observation.wallet_id == 43
    end

    test "update_observation/2 with invalid data returns error changeset" do
      observation = observation_fixture()
      assert {:error, %Ecto.Changeset{}} = Stream.update_observation(observation, @invalid_attrs)
      assert observation == Stream.get_observation!(observation.id)
    end

    test "delete_observation/1 deletes the observation" do
      observation = observation_fixture()
      assert {:ok, %Observation{}} = Stream.delete_observation(observation)
      assert_raise Ecto.NoResultsError, fn -> Stream.get_observation!(observation.id) end
    end

    test "change_observation/1 returns a observation changeset" do
      observation = observation_fixture()
      assert %Ecto.Changeset{} = Stream.change_observation(observation)
    end
  end
end
