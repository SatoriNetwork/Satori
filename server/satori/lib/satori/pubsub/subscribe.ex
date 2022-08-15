defmodule Satori.PubSub.Subscribe do
  alias __MODULE__.{Input, Output}

  @spec subscribe(Input.t()) :: Output.t()
  def subscribe(_input) do
    %Output{
      error: nil
    }
  end
end
