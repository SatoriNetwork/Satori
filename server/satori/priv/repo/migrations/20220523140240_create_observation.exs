defmodule Satori.Repo.Migrations.CreateObservation do
  use Ecto.Migration

  def change do
    create table(:observation) do
      add :wallet_id, :integer
      add :stream_id, :integer
      add :target_id, :integer
      add :value, :string

      timestamps()
    end
  end
end
