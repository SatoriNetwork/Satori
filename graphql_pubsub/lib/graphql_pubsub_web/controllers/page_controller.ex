defmodule GraphqlPubsubWeb.PageController do
  use GraphqlPubsubWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
