import unittest

from app.main import app


class PostsRouterTests(unittest.TestCase):
    def test_posts_router_is_registered(self) -> None:
        openapi_paths = set(app.openapi().get("paths", {}).keys())
        self.assertIn("/api/v1/posts/", openapi_paths)
        self.assertIn("/api/v1/posts/{post_id}", openapi_paths)


if __name__ == "__main__":
    unittest.main()
