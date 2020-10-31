# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Index of docker images and versions.
"""
import os
import logging
import yaml

from aswfdocker import constants, utils, versioninfo

logger = logging.getLogger(__name__)


class Index:
    """
    This is the index of all current package, images and versions.
    The data comes from the "versions.yaml" file at the root of the git repository.
    """

    def __init__(self):
        versions_file_path = os.path.join(utils.get_git_top_level(), "versions.yaml")
        with open(versions_file_path) as f:
            self._versions = yaml.load(f, Loader=yaml.FullLoader)
        self._version_infos = {}
        for version, v in self._versions["versions"].items():
            self._version_infos[version] = versioninfo.VersionInfo(
                version=version,
                major_version=v.get("major_version"),
                tags=v.get("tags", []),
                ci_common_version=v.get("ci_common_version"),
                package_versions=v.get("package_versions", {}),
                parent_versions=v.get("parent_versions", []),
                use_major_version_as_tag=v.get("use_major_version_as_tag", False),
            )
        for vi in self._version_infos.values():
            vi.all_package_versions = vi.package_versions.copy()
            for parent in vi.parent_versions:
                vi.all_package_versions.update(
                    self._version_infos[parent].package_versions
                )

    def _get_key(self, image_type: constants.ImageType):
        if image_type == constants.ImageType.PACKAGE:
            return "ci-packages"
        return "ci-images"

    def iter_images(self, image_type: constants.ImageType):
        """
        Iterates over all images by image type.
        """
        for image in self._versions[self._get_key(image_type)]:
            yield image

    def iter_versions(self, image_type: constants.ImageType, name: str):
        """
        Iterates over all versions by image type and image name.
        """
        for version in self._versions[self._get_key(image_type)][name]:
            yield version

    def iter_version_info(self):
        return self._version_infos.values()

    def version_info(self, version):
        for vi in self.iter_version_info():
            if version == vi.version:
                return vi
        raise ValueError("VersionInfo not found for version {}".format(version))
