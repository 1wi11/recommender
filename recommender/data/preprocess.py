from typing import Tuple, Dict

import pandas as pd

# explicit 평점(1~5)을 implicit feedback으로 변환한다.
# MovieLens 같은 평점 데이터는 원래 explicit인데, 대부분의 추천 모델은
# "관심 있다/없다"의 implicit 신호로 학습한다.
# 낮은 평점(1~2)은 "봤는데 싫었다"이지 "관심 있다"가 아니므로,
# threshold 이상(보통 4점)만 긍정 상호작용으로 남기고 rating 컬럼은 버린다.
def to_implicit(df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    return df[df["rating"] >= threshold][["user_id", "item_id", "timestamp"]].copy()


# 상호작용이 너무 적은 유저와 아이템을 걸러낸다.
# 영화 1편만 본 유저, 1명만 본 영화는 패턴을 학습할 수 없어서 노이즈가 된다.
# 유저를 제거하면 아이템 카운트가 줄고, 아이템을 제거하면 유저 카운트가 줄기 때문에
# 한 번으로 안 끝나고 변화가 없을 때까지 반복해야 한다. (k-core decomposition)
def filter_kcore(df: pd.DataFrame, min_user: int, min_item: int) -> pd.DataFrame:
    prev_len = -1

    while len(df) != prev_len:
        prev_len = len(df)

        user_counts = df["user_id"].value_counts()
        valid_users = user_counts[user_counts >= min_user].index
        df = df[df["user_id"].isin(valid_users)]

        item_counts = df["item_id"].value_counts()
        valid_items = item_counts[item_counts >= min_item].index
        df = df[df["item_id"].isin(valid_items)]

    return df.reset_index(drop=True)


# k-core 필터링 후 유저/아이템 ID에 구멍이 생긴다. (예: 1, 3, 7, 15...)
# 나중에 user-item 행렬을 만들 때 빈 행/열이 생기지 않도록
# 0부터 시작하는 연속 정수로 다시 매긴다.
# 원본 ID → 새 ID 매핑(user_map, item_map)도 같이 반환해서
# 나중에 원래 ID로 복원할 수 있게 한다.
def reindex_ids(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[int, int], Dict[int, int]]:
    user_ids = sorted(df["user_id"].unique())
    item_ids = sorted(df["item_id"].unique())

    user_map = {old: new for new, old in enumerate(user_ids)}
    item_map = {old: new for new, old in enumerate(item_ids)}

    df = df.assign(
        user_id=df["user_id"].map(user_map),
        item_id=df["item_id"].map(item_map),
    )

    return df, user_map, item_map
