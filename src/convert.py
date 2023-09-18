# http://bird.nae-lab.org/cattle/

import csv
import os
import shutil
from collections import defaultdict
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Cattle detection in UAV images"
    dataset_path = "/mnt/d/datasetninja-raw/cattle-detection-and-counting-in-uav-images"
    bbox_ext = ".txt"
    # ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        if ds_name == "Dataset1":
            im_data = image_path[-18:].replace("/", "\\")
        else:
            im_data = get_file_name_with_ext(image_path)
        bboxes_data = curr_ds_data[im_data]

        for bboxes in bboxes_data:
            tags = []
            if len(bboxes[0]) == 0:
                continue

            if len(bboxes[2]) == 0:
                continue

            left = int(bboxes[0])
            right = int(bboxes[0]) + int(bboxes[2])
            top = int(bboxes[1])
            bottom = int(bboxes[1]) + int(bboxes[3])
            rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)

            if len(bboxes[4]) != 0:
                quality_label = sly.Tag(tag_quality_label, value=quality[int(bboxes[4])])
                tags.append(quality_label)
            if len(bboxes[5]) != 0:
                cattle_id = sly.Tag(tag_cattle_id, value=int(bboxes[5]))
                tags.append(cattle_id)
            if len(bboxes[6]) != 0:
                id_conf_value = id_conf.get(int(bboxes[6]))
                if id_conf_value is not None:
                    id_conf_data = sly.Tag(tag_id_conf, value=id_conf_value)
                    tags.append(id_conf_data)

            label = sly.Label(rectangle, obj_class, tags=tags)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class = sly.ObjClass("cattle", sly.Rectangle)

    tag_quality_label = sly.TagMeta(
        "quality label",
        sly.TagValueType.ONEOF_STRING,
        possible_values=["Normal", "Truncated", "Blurred", "Occluded"],
    )
    tag_cattle_id = sly.TagMeta("cattle id", sly.TagValueType.ANY_NUMBER)
    tag_id_conf = sly.TagMeta(
        "id conf",
        sly.TagValueType.ONEOF_STRING,
        possible_values=["lack of confidence", "high confidence"],
    )

    quality = {0: "Normal", 1: "Truncated", 2: "Blurred", 3: "Occluded"}
    id_conf = {0: "lack of confidence", 1: "high confidence"}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class], tag_metas=[tag_quality_label, tag_id_conf, tag_cattle_id]
    )
    api.project.update_meta(project.id, meta.to_json())

    ds1_img_to_data = defaultdict(list)
    with open(os.path.join(dataset_path, "dataset1_annotation.csv"), "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            img_data = []
            if idx == 0:
                continue
            curr_row_data = row[0].split("\t")
            need_row_data = curr_row_data[2:]
            for i in range(0, len(need_row_data), 7):
                img_data.append(need_row_data[i : i + 7])

            ds1_img_to_data[curr_row_data[0]] = img_data

    ds2_img_to_data = defaultdict(list)
    with open(os.path.join(dataset_path, "dataset2_annotation.csv"), "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            img_data = []
            if idx == 0:
                continue
            curr_row_data = row[0].split("\t")
            need_row_data = curr_row_data[2:]
            for i in range(0, len(need_row_data), 7):
                img_data.append(need_row_data[i : i + 7])

            ds2_img_to_data[curr_row_data[0]] = img_data

    ds_to_data = {"Dataset1": ds1_img_to_data, "Dataset2": ds2_img_to_data}

    for ds_name in os.listdir(dataset_path):
        ds_path = os.path.join(dataset_path, ds_name)
        if dir_exists(ds_path):
            curr_ds_data = ds_to_data[ds_name]
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

            images_names = list(curr_ds_data.keys())

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                img_pathes_batch = [
                    os.path.join(ds_path, im_name.replace("\\", "/")) for im_name in img_names_batch
                ]

                if ds_name == "Dataset1":
                    img_names_batch = [im_name.replace("\\", "_") for im_name in img_names_batch]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(img_names_batch))
    return project
