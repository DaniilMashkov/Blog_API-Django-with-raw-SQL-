import random

from django.contrib.auth.hashers import make_password
from django.db import connection
from django.utils import timezone


class TestDataRepository:

    @staticmethod
    def get_admin_user_id(username):
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM auth_user WHERE username = %s', [username])
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def create_or_update_admin_user(username, email, first_name, password):
        admin_id = TestDataRepository.get_admin_user_id(username)
        if admin_id:
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE auth_user SET email = %s, first_name = %s, last_name = %s, password = %s, '
                    'is_superuser = %s, is_staff = %s, is_active = %s, date_joined = %s WHERE id = %s',
                    [email, first_name, '', make_password(password), True, True, True, timezone.now(), admin_id]
                )
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO auth_user (username, email, first_name, last_name, password, is_superuser, is_staff, is_active, date_joined) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [username, email, first_name, '', make_password(password), True, True, True, timezone.now()]
                )
            return cursor.lastrowid
        return admin_id

    @staticmethod
    def delete_all_comments():
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM comment')

    @staticmethod
    def delete_all_posts():
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM post')

    @staticmethod
    def create_post(title, description, text, author_id):
        created_date = timezone.now() - timezone.timedelta(days=random.randint(0, 30))
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO post (title, description, text, created, author_id) '
                'VALUES (%s, %s, %s, %s, %s) RETURNING id',
                [title, description, text, created_date, author_id]
            )
            return cursor.fetchone()[0]

    @staticmethod
    def create_comment(body, post_id, author):
        created_date = timezone.now() - timezone.timedelta(days=random.randint(0, 30))
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO comment (body, created, post_id, author) VALUES (%s, %s, %s, %s)',
                [body, created_date, post_id, author]
            )
