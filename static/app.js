document.addEventListener("DOMContentLoaded", () => {
  const eventsList = document.getElementById("events-list");

  // Fetch the events from the API
  fetch("/webhook/events")
    .then((response) => response.json())
    .then((data) => {
      if (data.length === 0) {
        eventsList.innerHTML = "<li><em>No events found.</em></li>";
      } else {
        data.forEach((event) => {
          const li = document.createElement("li");

          // Format the event display text based on the action type
          if (event.event === "PUSH") {
            li.innerHTML = `<em>"${event.author}" pushed to "${event.to_branch}" on ${event.timestamp}</em>`;
          } else if (event.event === "PULL_REQUEST") {
            li.innerHTML = `<em>"${event.author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${event.timestamp}</em>`;
          } else if (event.event === "MERGE") {
            li.innerHTML = `<em>"${event.author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${event.timestamp}</em>`;
          }

          eventsList.appendChild(li);
        });
      }
      console.log("Events fetched and rendered successfully."); // Log success message
    })
    .catch((error) => {
      console.error("Error fetching events:", error);
      eventsList.innerHTML = "<li><em>Error loading events.</em></li>";
    });

  // Set an interval to refresh the page every 15 seconds
  setInterval(() => {
    console.log("Refreshing the page...");
    window.location.reload();
  }, 15000);
});
