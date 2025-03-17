from locust import HttpUser, task, between

class ProjectPerfTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def home_page(self):
        """
        Represents a task for making a GET request to the home page endpoint.

        This function sends a GET request to the root ("/") of the server,
        typically used to simulate accessing the main entry point of a web application.
        It is commonly used in load testing scenarios to measure and analyze
        the performance and behavior of the home page under simulated user workloads.
        """
        self.client.get("/")

    @task
    def login_and_view_competitions(self):
        """
        Logs in the user and retrieves available competitions for viewing.

        This task simulates user login via a POST request and fetches competition
        details by sending an email as part of the request. It demonstrates user
        interactions with the application's login and competition viewing mechanism.
        """
        self.client.post("/showSummary", data={"email": "valid@email.com"})

    @task
    def book_places(self):
        """
        Posts a request to purchase a specified number of places for a given competition
        by a particular club. This method simulates the interaction with the server to
        purchase places for test purposes.
        """
        self.client.post("/purchasePlaces", data={
            "competition": "Future Competition",
            "club": "Test Club",
            "places": "2"
        })

    @task
    def view_clubs(self):
        """
        Represents a task to view clubs in the system.

        This method performs an HTTP GET request to fetch a list of clubs from the
        specified endpoint. It is typically used in scenarios involving performance
        testing or validation of the clubs-related API.
        """
        self.client.get("/clubs")

    @task
    def logout(self):
        """
        Logs the user out by sending a GET request to the "/logout" endpoint.

        This method simulates the user logging out of a system by sending an HTTP
        GET request to the logout endpoint. It is typically part of a larger
        test or load testing script, ensuring that user sessions are properly
        terminated.
        """
        self.client.get("/logout")