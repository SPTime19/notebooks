import json
from pathlib import Path


def agg_jsonls(folder_path: str):
    files = [file for file in Path(folder_path).rglob("*.jl")]
    ad_ls = []
    for file in files:
        for ad in file.open("r", encoding="utf-8"):
            ad_ls.append(json.loads(ad))
    return ad_ls


def load_dataset(folder_path: str):
    """
    Load unique reviews from data folder path
    :return:
    """
    # Unique reviews
    unique_ids = set()
    reviewsRA = []

    for complaint in agg_jsonls(folder_path):
        if "review_ID" in complaint and complaint["review_ID"] not in unique_ids:
            unique_ids.add(complaint["review_ID"])
            reviewsRA.append(complaint)

    return reviewsRA
