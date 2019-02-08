from . import BaseTest


class TestHome(BaseTest):
    """class to test home route"""
    def test_home_route(self):
        """tests response of home route"""
        resp = self.client.get(path="/api/v1/")
        self.assertEqual(resp.status_code, 200)
        