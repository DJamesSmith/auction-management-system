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


    // Preview the selected image
    let predictionTimer = null;

    // Preview selected image
    $("#auctionImage").on("change", function() {
        const file = this.files[0];

        if (predictionTimer) {
            clearTimeout(predictionTimer);
            predictionTimer = null;
        }

        if (file) {
            $("#imagePreview").attr("src", URL.createObjectURL(file));
            $("#imagePreviewContainer").show();
        } else {
            $("#imagePreview").attr("src", "");
            $("#imagePreviewContainer").hide();
        }

        $("#predictionId").val("");
        $("#predictionResult").hide();
        $("#manualCategoryContainer").show();
        $("#manualCategory").prop("required", true);
    });

    // Start category prediction
    $("#predictCategoryBtn").click(function(e) {
        e.preventDefault();
        const imageFile = $("#auctionImage")[0].files[0];

        if (!imageFile) {
            alert("Please select an image first.");
            return;
        }

        const formData = new FormData();
        formData.append("image", imageFile);
        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());

        $("#predictCategoryBtn").prop("disabled", true).text("Starting...");
        $("#predictionResult").text("⏳ Pending...").show();

        $.ajax({
            url: "/auctions/predict-category/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,

            success: function(response) {
                $("#predictCategoryBtn").prop("disabled", false).text("Predict Category");

                if (response.success) {
                    $("#predictionId").val(response.prediction_id);
                    $("#imagePreview").attr("src", response.image_url);
                    $("#imagePreviewContainer").show();
                    $("#predictionResult").text("⏳ Pending...").show();

                    checkAuctionPredictionStatus(response.prediction_id);
                } else {
                    showManualCategory(response.message);
                }
            },

            error: function(error) {
                $("#predictCategoryBtn").prop("disabled", false).text("Predict Category");

                const message = error.responseJSON && error.responseJSON.message
                    ? error.responseJSON.message
                    : "Could not start prediction. Please select a category manually.";

                showManualCategory(message);
            }
        });
    });

    // Poll prediction status
    function checkAuctionPredictionStatus(predictionId) {
        $.ajax({
            url: `/auctions/prediction-status/${predictionId}/`,
            type: "GET",

            success: function(response) {
                console.log("Auction prediction status:", response.status);

                if (response.status === "PENDING") {
                    $("#predictionResult").text("⏳ Pending...");
                    predictionTimer = setTimeout(function() {
                        checkAuctionPredictionStatus(predictionId);
                    }, 3000);
                }

                else if (response.status === "PROCESSING") {
                    $("#predictionResult").text("🔄 Processing image...");
                    predictionTimer = setTimeout(function() {
                        checkAuctionPredictionStatus(predictionId);
                    }, 3000);
                }

                else if (response.status === "COMPLETED") {
                    $("#predictionResult").html(
                        "<strong>Predicted Category:</strong> " +
                        $("<div>").text(response.category).html() +
                        "<br><strong>Confidence:</strong> " +
                        response.confidence + "%"
                    );

                    $("#manualCategoryContainer").hide();
                    $("#manualCategory").prop("required", false).val("");
                }

                else if (response.status === "FAILED") {
                    showManualCategory("❌ Prediction failed. Please select a category manually.");
                }
            },

            error: function(error) {
                console.log("Status check failed:", error);
                $("#predictionResult").text("Unable to check prediction status. Please try again.");
            }
        });
    }

    // Show manual category selection on failure
    function showManualCategory(message) {
        if (predictionTimer) {
            clearTimeout(predictionTimer);
            predictionTimer = null;
        }

        $("#predictionId").val("");
        $("#predictionResult").text(message).show();
        $("#manualCategoryContainer").show();
        $("#manualCategory").prop("required", true);
    }

});