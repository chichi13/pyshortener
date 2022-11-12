import random

from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    # Please, do not DOS website, uncomment the commented line in redirect_link function of link/routes.py
    @task(1)
    def create_links(self):
        self.client.post(
            "/links",
            json={
                "long_url": "https://localhost.com/"
            }
        )

    @task(2)
    def get_link(self):
        link = random.choice(["biPaVA", "PjZf2s", "HtWHDF", "Xe17VH", "false_shortcode"])
        self.client.get(f"/{link}")
