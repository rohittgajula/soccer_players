from locust import HttpUser, task, between

class PlayerLoadTest(HttpUser):
    wait_time = between(1, 5)
    player_ids = []  # Store player IDs

    def on_start(self):
        # Fetch player IDs from the newly created API endpoint
        response = self.client.get("/api/player-ids/")
        if response.status_code == 200:
            self.player_ids = response.json()  # Store player IDs directly from the response

    @task
    def get_player(self):
        if self.player_ids:
            # Sequentially pick a player ID from the list
            for player_id in self.player_ids:
                self.client.get(f"/api/players/{player_id}/")
