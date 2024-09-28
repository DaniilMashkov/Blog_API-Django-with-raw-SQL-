from django.core.management import BaseCommand
from faker import Faker

from posts.repository.test_data_repository import TestDataRepository

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        admin_id = TestDataRepository.create_or_update_admin_user('admin', 'admin@test.com', 'admin', 'admin')

        TestDataRepository.delete_all_comments()
        TestDataRepository.delete_all_posts()

        for i in range(1, 31):
            post_title = f'Post {i}'
            post_description = fake.sentence(nb_words=4)
            post_text = fake.sentence(nb_words=30)

            post_id = TestDataRepository.create_post(post_title, post_description, post_text, admin_id)

            for j in range(1, 11):
                comment_text = fake.sentence(nb_words=15)
                author = f'Author {j}'
                TestDataRepository.create_comment(comment_text, post_id, author)

        self.stdout.write(self.style.SUCCESS('Admin, posts and comments successfully created'))
