import json
from pathlib import Path

from omegaconf import DictConfig

from recommender.data.loader import load_ratings
from recommender.data.preprocess import to_implicit, filter_kcore, reindex_ids
from recommender.data.split import leave_one_out


def run(cfg: DictConfig) -> None:
    data_root = cfg.paths.data_root
    dataset_name = cfg.dataset.name
    variant = cfg.dataset.variant
    preprocess = cfg.preprocess

    base_dir = Path(data_root) / dataset_name / variant
    processed_dir = base_dir / "processed"
    splits_dir = base_dir / "splits"
    processed_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)

    # 1. 원본 데이터 로드
    print(f"Loading {dataset_name}/{variant}...")
    df = load_ratings(dataset_name, data_root, variant)
    print(f"  raw: {len(df)} interactions, {df['user_id'].nunique()} users, {df['item_id'].nunique()} items")

    # 2. implicit feedback 변환
    df = to_implicit(df, preprocess.rating_threshold)
    print(f"  after to_implicit (threshold={preprocess.rating_threshold}): {len(df)} interactions")

    # 3. k-core 필터링
    df = filter_kcore(df, preprocess.min_user_interactions, preprocess.min_item_interactions)
    print(f"  after k-core ({preprocess.min_user_interactions}/{preprocess.min_item_interactions}): {len(df)} interactions, {df['user_id'].nunique()} users, {df['item_id'].nunique()} items")

    # 4. ID 재인덱싱
    df, user_map, item_map = reindex_ids(df)
    print(f"  reindexed: user 0~{df['user_id'].max()}, item 0~{df['item_id'].max()}")

    # 5. 전처리 결과 저장
    df.to_csv(processed_dir / "interactions.csv", index=False)

    with open(processed_dir / "user_map.json", "w") as f:
        json.dump({str(k): v for k, v in user_map.items()}, f)

    with open(processed_dir / "item_map.json", "w") as f:
        json.dump({str(k): v for k, v in item_map.items()}, f)

    # 6. train/val/test 분리
    train, val, test = leave_one_out(df)
    print(f"  split: train={len(train)}, val={len(val)}, test={len(test)}")

    train.to_csv(splits_dir / "train.csv", index=False)
    val.to_csv(splits_dir / "val.csv", index=False)
    test.to_csv(splits_dir / "test.csv", index=False)

    print(f"Saved to {processed_dir} and {splits_dir}")
