from typing import Tuple

import pandas as pd


# 유저별로 가장 마지막 상호작용을 test, 그 직전을 val, 나머지를 train으로 나눈다.
# 추천 시스템에서 가장 흔히 쓰이는 leave-one-out 방식이다.
# 시간순으로 나누는 이유는, 실제 서비스에서도 과거 데이터로 미래를 예측하기 때문이다.
# random split을 하면 미래 정보가 학습에 섞여서 성능이 과대평가된다. (data leakage)
def leave_one_out(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.sort_values(["user_id", "timestamp"])

    # 유저별로 마지막 2개를 떼어내기 위해 역순 rank를 매긴다.
    df = df.assign(
        rank=df.groupby("user_id").cumcount(ascending=False)
    )

    test = df[df["rank"] == 0].drop(columns=["rank"])
    val = df[df["rank"] == 1].drop(columns=["rank"])
    train = df[df["rank"] >= 2].drop(columns=["rank"])

    return train, val, test
