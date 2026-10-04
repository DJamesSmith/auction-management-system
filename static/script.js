$(document).ready(function () {

    console.log("Auction timer jquery is running");

    $(".countdown").each(function () {

        let timerElement = $(this);
        let auctionId = timerElement.data("auction-id");

        console.log("Starting timer for auction:", auctionId);

        $.ajax({

            url: "/auctions/timer/" + auctionId + "/",
            type: "GET",

            success: function (response) {

                console.log(response);

                if (response.status) {

                    let startTime = new Date(response.start_datetime).getTime();

                    let timer = setInterval(function () {

                        let now = new Date().getTime();

                        let distance = startTime - now;

                        if (distance <= 0) {

                            clearInterval(timer);

                            timerElement.text("00:00:00");

                            return;
                        }

                        let hours = Math.floor(
                            distance / (1000 * 60 * 60)
                        );

                        let minutes = Math.floor(
                            (distance % (1000 * 60 * 60))
                            / (1000 * 60)
                        );

                        let seconds = Math.floor(
                            (distance % (1000 * 60))
                            / 1000
                        );

                        timerElement.text(
                            hours + ":" +
                            String(minutes).padStart(2, "0") + ":" +
                            String(seconds).padStart(2, "0")
                        );

                    }, 1000);
                }
            },

            error: function (error) {

                console.log(error);

                timerElement.text("Unable to load timer");

            }
        });

    });

});