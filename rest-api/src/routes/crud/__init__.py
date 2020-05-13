from .posts import Post

def init_crud(api):
    print("Init Auth")
    api.add_resource(Post, '/api/crud/post')