document.addEventListener("DOMContentLoaded", function () {
    const reviewForm = document.getElementById("review_form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let formData = new FormData(this);
            let rating = formData.get("rating");
            let comment = formData.get("comment");
            let url = this.action;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ rating, comment }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let reviewContainer = document.getElementById("reviews");
                    let noReviewsMessage = document.getElementById("no_reviews");

                    if (noReviewsMessage) {
                        noReviewsMessage.remove();
                    }

                    let newReview = document.createElement("p");
                    newReview.innerHTML = `<strong>${data.user}</strong>: ★ ${data.rating} - ${data.comment} - ${data.timestamp}`;
                    reviewContainer.prepend(newReview);

                    document.getElementById("review_form").reset();
                } else {
                    alert("Error submitting review: " + data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
