from .posts import Posts

def init_crud(api):
    print("Init Auth")
    api.add_resource(Posts, '/api/crud/posts')