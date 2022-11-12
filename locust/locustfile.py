import random

from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    # wait_time = between(1, 4)

    # @task(1)
    # def get_link(self):
    #     link = random.choice(["DJ9Ndw", "mdQn6M", "false_shortcode"])
    #     self.client.get(f"/{link}")

    @task(2)
    def create_links(self):
        self.client.post(
            "/links",
            json={
                "long_url": "https://localhost.com/"
            }
        )
