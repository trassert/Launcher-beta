"fabric contains functions for dealing with the `Fabric modloader <https://fabricmc.net/>`_."
from ._helper import download_file, get_requests_response_cache, parse_maven_metadata, empty
from .exceptions import VersionNotFound, UnsupportedVersion, ExternalProgramError
from .types import FabricMinecraftVersion, FabricLoader, CallbackDict
from .install import install_minecraft_version
from typing import List, Optional, Union
from .utils import is_version_valid
import subprocess
import tempfile
import random
import os
def get_all_minecraft_versions() -> List[FabricMinecraftVersion]:
    """
    Returns all available Minecraft Versions for Fabric
    Example:
    .. code:: python
        for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions():
            print(version["version"])
    """
    FABRIC_MINECARFT_VERSIONS_URL = "https://meta.fabricmc.net/v2/versions/game"
    return get_requests_response_cache(FABRIC_MINECARFT_VERSIONS_URL).json()
def get_stable_minecraft_versions() -> List[str]:
    """
    Returns a list which only contains the stable Minecraft versions that supports Fabric
    Example:
    .. code:: python
        for version in minecraft_launcher_lib.fabric.get_stable_minecraft_versions():
            print(version)
    """
    minecraft_versions = get_all_minecraft_versions()
    stable_versions = []
    for i in minecraft_versions:
        if i["stable"] is True:
            stable_versions.append(i["version"])
    return stable_versions
def get_latest_minecraft_version() -> str:
    """
    Returns the latest unstable Minecraft versions that supports Fabric. This could be a snapshot.
    Example:
    .. code:: python
        print("Latest Minecraft version: " + minecraft_launcher_lib.fabric.get_latest_minecraft_version())
    """
    minecraft_versions = get_all_minecraft_versions()
    return minecraft_versions[0]["version"]
def get_latest_stable_minecraft_version() -> str:
    """
    Returns the latest stable Minecraft version that supports Fabric
    Example:
    .. code:: python
        print("Latest stable Minecraft version: " + minecraft_launcher_lib.fabric.get_latest_stable_minecraft_version())
    """
    stable_versions = get_stable_minecraft_versions()
    return stable_versions[0]
def is_minecraft_version_supported(version: str) -> bool:
    """
    Checks if a Minecraft version supported by Fabric
    Example:
    .. code:: python
        version = "1.20"
        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
            print(f"{version} is supported by fabric")
        else:
            print(f"{version} is not supported by fabric")
    :param version: A vanilla version
    """
    minecraft_versions = get_all_minecraft_versions()
    for i in minecraft_versions:
        if i["version"] == version:
            return True
    return False
def get_all_loader_versions() -> List[FabricLoader]:
    """
    Returns all loader versions
    Example:
    .. code:: python
        for version in minecraft_launcher_lib.fabric.get_all_loader_versions():
            print(version["version"])
    """
    FABRIC_LOADER_VERSIONS_URL = "https://meta.fabricmc.net/v2/versions/loader"
    return get_requests_response_cache(FABRIC_LOADER_VERSIONS_URL).json()
def get_latest_loader_version() -> str:
    """
    Get the latest loader version
    Example:
    .. code:: python
        print("Latest loader version: " + minecraft_launcher_lib.fabric.get_latest_loader_version())
    """
    loader_versions = get_all_loader_versions()
    return loader_versions[0]["version"]
def get_latest_installer_version() -> str:
    """
    Returns the latest installer version
    Example:
    .. code:: python
        print("Latest installer version: " + minecraft_launcher_lib.fabric.get_latest_installer_version())
    """
    FABRIC_INSTALLER_MAVEN_URL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml"
    return parse_maven_metadata(FABRIC_INSTALLER_MAVEN_URL)["latest"]
def install_fabric(minecraft_version: str, minecraft_directory: Union[str, os.PathLike], loader_version: Optional[str] = None, callback: Optional[CallbackDict] = None, java: Optional[Union[str, os.PathLike]] = None) -> None:
    """
    Installs the Fabric modloader.
    For more information take a look at the :doc:`tutorial </tutorial/install_fabric>`.
    Example:
    .. code:: python
        minecraft_version = "1.20"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory)
    :param minecraft_version: A vanilla version that is supported by Fabric
    :param minecraft_directory: The path to your Minecraft directory
    :param loader_version: The fabric loader version. If not given it will use the latest
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param java: A Path to a custom Java executable
    :raises VersionNotFound: The given Minecraft does not exists
    :raises UnsupportedVersion: The given Minecraft version is not supported by Fabric
    """
    path = str(minecraft_directory)
    if not callback:
        callback = {}
    if not is_version_valid(minecraft_version, minecraft_directory):
        raise VersionNotFound(minecraft_version)
    if not is_minecraft_version_supported(minecraft_version):
        raise UnsupportedVersion(minecraft_version)
    if not loader_version:
        loader_version = get_latest_loader_version()
    install_minecraft_version(minecraft_version, path, callback=callback)
    installer_version = get_latest_installer_version()
    installer_download_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"
    installer_path = os.path.join(tempfile.gettempdir(), f"fabric-installer-{random.randrange(100, 10000)}.tmp")
    download_file(installer_download_url, installer_path, callback=callback)
    callback.get("setStatus", empty)("Running fabric installer")
    command = ["java" if java is None else str(java), "-jar", installer_path, "client", "-dir", path, "-mcversion", minecraft_version, "-loader", loader_version, "-noprofile", "-snapshot"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ExternalProgramError(command, result.stdout, result.stderr)
    os.remove(installer_path)
    fabric_minecraft_version = f"fabric-loader-{loader_version}-{minecraft_version}"
    install_minecraft_version(fabric_minecraft_version, path, callback=callback)
