defmodule GraphqlPubsubWeb.Router do
  use GraphqlPubsubWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
    plug GraphqlPubsubWeb.Plugs.SetCurrentUser
  end

  scope "/" do
    pipe_through :api

    forward "/api", Absinthe.Plug,
      schema: GraphqlPubsubWeb.Schema.Schema

    forward "/satori", Absinthe.Plug.GraphiQL,
    schema: GraphqlPubsubWeb.Schema.Schema,
    socket: GraphqlPubsubWeb.UserSocket

    # forward "/graphiql", Absinthe.Plug.GraphiQL,
    #   schema: GraphqlPubsubWeb.Schema.Schema,
    #   socket: GraphqlPubsubWeb.UserSocket
    end


end
