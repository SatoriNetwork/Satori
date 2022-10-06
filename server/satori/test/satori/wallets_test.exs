defmodule Satori.WalletsTest do
  use Satori.DataCase

  alias Satori.Wallets

  describe "wallets" do
    alias Satori.Wallets.Wallet

    import Satori.WalletsFixtures

    @invalid_attrs %{address: nil, public_key: nil, user_id: nil}

    # test "list_wallets/0 returns all wallets" do
    #   wallet = wallet_fixture()
    #   assert Wallets.list_wallets() == [wallet]
    # end

    describe "list_wallets/1" do
      test "returns all wallets by default" do
        wallet = wallet_fixture()

        results = Wallets.list_wallets([])

        assert length(results) == length(wallet)
      end

      test "returns limited number of wallets" do
        wallet_fixture()

        criteria = %{limit: 1}

        results = Wallets.list_wallets(criteria)

        assert length(results) == 1
      end

      test "returns limited and ordered wallets" do
        wallet_fixture()

        args = %{limit: 3, order: :desc}

        results = Wallets.list_wallets(args)

        assert Enum.map(results, &(&1.address)) == ["Wallet 3", "Wallet 2", "Wallet 1"]
      end

      test "returns wallets filtered by matching address" do
        wallet_fixture()

        criteria = %{filter: %{matching: "1"}}

        results = Wallets.list_wallets(criteria)

        assert Enum.map(results, &(&1.address)) == ["Wallet 1"]
      end

      test "returns wallets filtered by public_key" do
        wallet_fixture()

        criteria = %{filter: %{public_key: "1"}}

        results = Wallets.list_wallets(criteria)

        assert Enum.map(results, &(&1.address)) == ["Wallet 2", "Wallet 3"]
      end
    end

    test "get_wallet!/1 returns the wallet with given id" do
      wallet = wallet_fixture()
      assert Wallets.get_wallet!(wallet.id) == wallet
    end

    test "create_wallet/1 with valid data creates a wallet" do
      valid_attrs = %{address: "some address", public_key: "some public_key", user_id: 42}

      assert {:ok, %Wallet{} = wallet} = Wallets.create_wallet(valid_attrs)
      assert wallet.address == "some address"
      assert wallet.public_key == "some public_key"
      assert wallet.user_id == 42
    end

    test "create_wallet/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Wallets.create_wallet(@invalid_attrs)
    end

    test "update_wallet/2 with valid data updates the wallet" do
      wallet = wallet_fixture()
      update_attrs = %{address: "some updated address", public_key: "some updated public_key", user_id: 43}

      assert {:ok, %Wallet{} = wallet} = Wallets.update_wallet(wallet, update_attrs)
      assert wallet.address == "some updated address"
      assert wallet.public_key == "some updated public_key"
      assert wallet.user_id == 43
    end

    test "update_wallet/2 with invalid data returns error changeset" do
      wallet = wallet_fixture()
      assert {:error, %Ecto.Changeset{}} = Wallets.update_wallet(wallet, @invalid_attrs)
      assert wallet == Wallets.get_wallet!(wallet.id)
    end

    test "delete_wallet/1 deletes the wallet" do
      wallet = wallet_fixture()
      assert {:ok, %Wallet{}} = Wallets.delete_wallet(wallet)
      assert_raise Ecto.NoResultsError, fn -> Wallets.get_wallet!(wallet.id) end
    end

    test "change_wallet/1 returns a wallet changeset" do
      wallet = wallet_fixture()
      assert %Ecto.Changeset{} = Wallets.change_wallet(wallet)
    end
  end
end
