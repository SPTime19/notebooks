import json
from pathlib import Path


def agg_jsonls(folder_path: str, file_ext="jl"):
    files = [file for file in Path(folder_path).rglob(f"*.{file_ext}")]
    ad_ls = []
    for file in files:
        try:
            for ad in file.open("r", encoding="utf-8"):
                ad_ls.append(json.loads(ad))
        except Exception as err:
            print(f"Error opening file {file}")
    return ad_ls


def load_dataset(folder_path: str, id_field: str = "review_ID", dataset_ext: str = "jl"):
    """
    Load unique reviews from data folder path
    :return:
    """
    # Unique reviews
    unique_ids = set()
    reviews = []

    for complaint in agg_jsonls(folder_path, dataset_ext):
        if id_field in complaint and complaint[id_field] not in unique_ids:
            unique_ids.add(complaint[id_field])
            reviews.append(complaint)

    return reviews
