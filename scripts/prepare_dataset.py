import hydra
from omegaconf import DictConfig

from recommender.pipelines.prepare import run


@hydra.main(
    version_base=None,
    config_path="../recommender/conf",
    config_name="config",
)
def main(cfg: DictConfig):
    run(cfg)


if __name__ == "__main__":
    main()
