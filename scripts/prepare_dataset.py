# scripts/prepare_dataset.py
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(
    version_base=None,
    config_path="../recommender/conf",
    config_name="config"
)
def main(cfg: DictConfig):
    print("===== FULL CONFIG =====")
    print(OmegaConf.to_yaml(cfg))

    print("===== KEY VALUES =====")
    print(f"dataset.name    : {cfg.dataset.name}")
    print(f"dataset.variant : {cfg.dataset.variant}")
    print(f"data_root       : {cfg.paths.data_root}")

    base_dir = (
        f"{cfg.paths.data_root}/"
        f"{cfg.dataset.name}/"
        f"{cfg.dataset.variant}"
    )

    print("===== DERIVED PATHS =====")
    print(f"base_dir      : {base_dir}")
    print(f"raw_dir       : {base_dir}/raw")
    print(f"processed_dir : {base_dir}/processed")
    print(f"splits_dir    : {base_dir}/splits")
    print(f"artifacts_dir : {base_dir}/artifacts")


if __name__ == "__main__":
    main()