class PostService:
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def get_post_with_comments(self, post_id):
        post_data = self.post_repository.get_post_detail(post_id)

        if not post_data:
            return None

        post_info = {
            'id': post_data[0][0],
            'title': post_data[0][1],
            'description': post_data[0][2],
            'text': post_data[0][3],
            'image': post_data[0][4],
            'created': post_data[0][5],
            'author': {
                'id': post_data[0][6],
                'username': post_data[0][7],
                'email': post_data[0][8],
            },
            'comments': []
        }

        for row in post_data:
            comment = {
                'id': row[9],
                'author': row[10],
                'body': row[11],
                'created': row[12],
            }
            if comment['id'] is not None:
                post_info['comments'].append(comment)

        return post_info

    def get_posts(self, author_id=None, order_by=None):
        posts = self.post_repository.get_posts(author_id, order_by)
        return self._format_posts(posts)

    def _format_posts(self, posts):
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                'id': post[0],
                'title': post[1],
                'description': post[2],
                'image': post[3],
                'created': post[4],
                'author': {
                    'id': post[5],
                    'username': post[6],
                    'email': post[7],
                },
                'last_comment_date': post[8],
                'last_comment_author': post[9],
            })
        return formatted_posts
