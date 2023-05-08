```bash
python gtsfm/runner/run_scene_optimizer_colmaploader.py --config_name deep_front_end.yaml --images_dir /mnt/DATA/Datasets/SFM/1DSFM/images.Gendarmenmarkt/Gendarmenmarkt/images/ --colmap_files_dirpath /mnt/DATA/Datasets/SFM/1DSFM/images.Gendarmenmarkt/Gendarmenmarkt/colmap_result/sparse/0 --max_frame_lookahead 10000000 --num_workers 2 --threads_per_worker 8 --max_resolution 640 --output_root /mnt/DATA/Datasets/SFM/1DSFM/images.Gendarmenmarkt/Gendarmenmarkt/gtsfm_result/ --mvs_off



python gtsfm/runner/run_scene_optimizer_colmaploader.py --config_name deep_front_end.yaml --images_dir /home/ydu318/sfm/data/1dsfm/Gendarmenmarkt/images/ --colmap_files_dirpath /home/ydu318/sfm/data/1dsfm/Gendarmenmarkt/colmap_result/sparse/0 --max_frame_lookahead 10000000 --num_workers 1 --threads_per_worker 8 --max_resolution 6000 --mvs_off


python gtsfm/runner/run_scene_optimizer_1dsfm.py --config_name deep_front_end.yaml --dataset_root /home/ydu318/sfm/data/1dsfm/Gendarmenmarkt/ --max_frame_lookahead 10000000 --num_workers 3 --threads_per_worker 8 --max_resolution 6000 --mvs_off --cluster_configs cluster.yaml

```