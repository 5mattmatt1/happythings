from .posts import Post, Posts

def init_crud(api):
    print("Init CRUD")
    api.add_resource(Post, '/api/crud/post')
    api.add_resource(Posts, '/api/crud/posts')