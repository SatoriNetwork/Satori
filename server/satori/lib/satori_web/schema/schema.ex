defmodule SatoriWeb.Schema.Schema do
  use Absinthe.Schema
  # alias Satori.Devices
  # alias Satori.Wallets

  import_types Absinthe.Type.Custom

  alias SatoriWeb.Resolvers

  # query {
  #   devices(limit: 2, order: DESC, filter: {matching: "mac", wallet_id: 3}) {
  #     id
  #     name
  #     cpu
  #     wallet_id
  #   }
  # }

  query do
    @desc "Get a device by its id"
    field :device, :device do
      arg :id, non_null(:string)
      resolve &Resolvers.Device.device/3
      # resolve fn _, %{id: id}, _ ->
      #   {:ok, Devices.get_device!(id)}
      # end
    end

    @desc "Get a list of devices"
    field :devices, list_of(:device) do
      arg :limit, :integer
      arg :order, type: :sort_order, default_value: :asc
      arg :filter, :place_filter
      resolve &Resolvers.Device.devices/3
      # resolve fn _, args, _ ->
      #   {:ok, Devices.list_devices(args)}
      # end
    end

    @desc "Get a Wallet by its id"
    field :wallet, :wallet do
      arg :id, non_null(:string)
      resolve &Resolvers.Wallet.wallet/3
    end

    @desc "Get a list of Wallets"
    field :wallets, list_of(:wallet) do
      arg :limit, :integer
      arg :order, type: :sort_order, default_value: :asc
      arg :filter, :place_filter
      resolve &Resolvers.Wallet.wallets/3
    end
  end

  input_object :place_filter do
    field :matching, :string
    field :ram, :integer
    field :address, :string
    field :public_key, :string
    # field :available_between, :date_range
  end

  # input_object :date_range do
  #   field :start_date, non_null(:date)
  #   field :end_date, non_null(:date)
  # end

  enum :sort_order do
    value :asc
    value :desc
  end

  object :device do
    field :id, non_null(:id)
    field :bandwidth, non_null(:string)
    field :cpu, non_null(:string)
    field :disk, non_null(:integer)
    field :name, non_null(:string)
    field :ram, non_null(:integer)
    field :wallet, list_of(:wallet) do
      resolve &Resolvers.Device.wallet_for_device/3
    end
  end

  object :wallet do
    field :id, non_null(:id)
    field :address, non_null(:string)
    field :public_key, non_null(:string)
    field :device, list_of(:device) do
      resolve &Resolvers.Wallet.device_for_wallet/3
    end
  end
end
