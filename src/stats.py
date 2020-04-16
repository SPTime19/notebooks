

def rundown_general_batch_stats(reviewsRA):
    reviews_with_response = [review for review in reviewsRA if
                             "responses" in review and len(review["responses"]["business"]) > 0]
    reviews_with_no_response = [review for review in reviewsRA if
                                "responses" in review and len(review["responses"]["business"]) == 0]

    print(
        f"Total of reviews with response {len(reviews_with_response)} [{round((len(reviews_with_response) / len(reviewsRA)) * 100, 2)}%]")
    print(
        f"Total of reviews with NO response {len(reviews_with_no_response)} [{100 - round((len(reviews_with_response) / len(reviewsRA)) * 100, 2)}%]")
    print(f"We have a total of {len(reviewsRA)} reviews!")

    