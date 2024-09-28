from django.db import connection


class PostRepository:

    def get_post_detail(self, post_id):
        with connection.cursor() as cursor:
            query = """
                SELECT
                    post.id, post.title, post.description, post.text, post.image, post.created,
                    post.author_id, auth_user.username, auth_user.email,
                    comment.id AS comment_id, comment.author AS comment_author,
                    comment.body AS comment_body, comment.created AS comment_created
                FROM
                    post
                INNER JOIN
                    auth_user ON post.author_id = auth_user.id
                LEFT JOIN
                    comment ON post.id = comment.post_id
                WHERE
                    post.id = %s
                ORDER BY
                    comment.created DESC
            """
            cursor.execute(query, [post_id])
            return cursor.fetchall()

    def get_posts(self, author_id=None, order_by=None):
        with connection.cursor() as cursor:
            query = """
                SELECT
                        post.id AS post_id,
                        post.title,
                        post.description,
                        post.image,
                        post.created AS post_created,
                        auth_user.id AS author_id,
                        auth_user.username,
                        auth_user.email,
                        (SELECT comment.created FROM comment
                            WHERE comment.post_id = post.id
                            ORDER BY comment.created DESC LIMIT 1) AS last_comment_date,
                        (SELECT comment.author FROM comment
                            WHERE comment.post_id = post.id
                            ORDER BY comment.created DESC LIMIT 1) AS last_comment_author
                    FROM
                        post
                    INNER JOIN
                        auth_user ON post.author_id = auth_user.id

                """
            params = []

            if author_id:
                query += " WHERE post.author_id = %s"
                params.append(author_id)

            if order_by == 'post_created':
                query += f" ORDER BY {order_by} DESC"
            if order_by == 'title':
                query += "ORDER BY NULLIF(REGEXP_REPLACE(post.title, '[^0-9]', '', 'g'), '')::INTEGER"

            cursor.execute(query, params)
            return cursor.fetchall()
