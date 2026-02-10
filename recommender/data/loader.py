from pathlib import Path

import pandas as pd


MOVIELENS_COLUMNS = ["user_id", "item_id", "rating", "timestamp"]
MOVIELENS_SEPARATOR = "::"


def load_movielens(data_root: str, variant: str) -> pd.DataFrame:
    path = Path(data_root) / "movielens" / variant / "raw" / "ratings.dat"

    if not path.exists():
        raise FileNotFoundError(f"ratings.dat not found: {path}")

    df = pd.read_csv(
        path,
        sep=MOVIELENS_SEPARATOR,
        header=None,
        names=MOVIELENS_COLUMNS,
        engine="python",
    )

    return df


DATASET_LOADERS = {
    "movielens": load_movielens,
}


def load_ratings(dataset_name: str, data_root: str, variant: str) -> pd.DataFrame:
    loader = DATASET_LOADERS.get(dataset_name)

    if loader is None:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available: {list(DATASET_LOADERS.keys())}"
        )

    return loader(data_root, variant)
