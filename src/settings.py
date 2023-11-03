from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Cattle Detection and Counting in UAV Images"
PROJECT_NAME_FULL: str = (
    "Cattle Detection and Counting in UAV Images Based on Convolutional Neural Networks"
)
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_ND_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Industry.Livestock(),
    Domain.DroneInspection(),
]
CATEGORY: Category = Category.Livestock(extra=Category.Drones())

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2020

HOMEPAGE_URL: str = "http://bird.nae-lab.org/cattle/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 4260609
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/cattle-detection-and-counting-in-uav-images"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Dataset1, images(3.17GB)": "http://bird.nae-lab.org/cattle/Dataset1.zip",
    "Dataset1, annotations": "http://bird.nae-lab.org/cattle/dataset1_annotation.txt",
    "Dataset2, images(72.9MB)": "http://bird.nae-lab.org/cattle/Dataset2.zip",
    "Dataset2, annotations": "http://bird.nae-lab.org/cattle/dataset1_annotation.txt",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[
    Union[str, List[str], Dict[str, str]]
] = "https://www.tandfonline.com/doi/full/10.1080/01431161.2019.1624858"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = "http://bird.nae-lab.org/cattle/"
AUTHORS: Optional[List[str]] = [
    "Wen Shao",
    "Rei Kawakami",
    "Ryota Yoshihashi",
    "Shaodi You",
    "Hidemichi Kawase",
    "Takeshi Naemura",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["shao@hc.ic.i.u-tokyo.ac.jp"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "The University of Tokyo",
    "Data61-CSIRO",
    "Kamiens Technology Inc",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.u-tokyo.ac.jp/en/",
    "https://www.csiro.au/en/about/people/business-units/data61",
    "http://www.kamiens.com/en/index.html",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "__PRETEXT__": "Additionally, every object contains information about ***cattle id***, ***quality label*** (Normal, Truncated, Blurred, or Occluded), ***id conf*** (lack of confidence or high confidence). Explore them in supervisely labeling tool"
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
