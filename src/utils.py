#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from shutil import copytree
import os, subprocess, sys

def permissions(parser, filename, *args, **kwargs):
    """Checks permissions using os.access() to see the user is authorized to access
    a file/directory. Checks for existence, readability, writability and executability via:
    os.F_OK (tests existence), os.R_OK (tests read), os.W_OK (tests write), os.X_OK (tests exec).
    @param parser <argparse.ArgumentParser() object>:
        Argparse parser object
    @param filename <str>:
        Name of file to check
    @return filename <str>:
        If file exists and user can read from file
    """
    if not exists(filename):
        parser.error("File '{}' does not exists! Failed to provide vaild input.".format(filename))

    if not os.access(filename, *args, **kwargs):
        parser.error("File '{}' exists, but cannot read file due to permissions!".format(filename))

    return filename


def exists(testpath):
    """Checks if file exists on the local filesystem.
    @param parser <argparse.ArgumentParser() object>:
        argparse parser object
    @param testpath <str>:
        Name of file/directory to check
    @return does_exist <boolean>:
        True when file/directory exists, False when file/directory does not exist
    """
    does_exist = True
    if not os.path.exists(testpath):
        does_exist = False # File or directory does not exist on the filesystem

    return does_exist


def ln(files, outdir):
    """Creates symlinks for files to an output directory.
    @param files list[<str>]:
        List of filenames
    @param outdir <str>:
        Destination or output directory to create symlinks
    """
    # Create symlinks for each file in the output directory
    for file in files:
        ln = os.path.join(outdir, os.path.basename(file))
        if not exists(ln):
                os.symlink(os.path.abspath(os.path.realpath(file)), ln)
        

def initialize(output_path, links=[]):
    """Initialize the output directory. If user provides a output
    directory path that already exists on the filesystem as a file 
    (small chance of happening but possible), a OSError is raised. If the
    output directory PATH already EXISTS, it will not try to create the directory.
    @param output_path <str>:
        Pipeline output path, created if it does not exist
    @param links list[<str>]:
        List of files to symlink into output_path
    """
    if not exists(output_path):
        # Pipeline output directory does not exist on filesystem
        os.makedirs(output_path)

    elif exists(output_path) and os.path.isfile(output_path):
        # Provided Path for pipeline output directory exists as file
        raise OSError("""\n\tFatal: Failed to create provided pipeline output directory!
        User provided --output PATH already exists on the filesystem as a file.
        Please run {} again with a different --output PATH.
        """.format(sys.argv[0])
        )
    
    # Create symlinks for each file in the output directory
    ln(links, output_path)
    


def which(cmd, path=None):
    """Checks if an executable is in $PATH
    @param cmd <str>:
        Name of executable to check
    @param path <list>:
        Optional list of PATHs to check [default: $PATH]
    @return <boolean>:
        True if exe in PATH, False if not in PATH
    """
    if path is None:
        path = os.environ["PATH"].split(os.pathsep)

    for prefix in path:
        filename = os.path.join(prefix, cmd)
        executable = os.access(filename, os.X_OK)
        is_not_directory = os.path.isfile(filename)
        if executable and is_not_directory:
            return True
    return False


def err(*message, **kwargs):
    """Prints any provided args to standard error.
    kwargs can be provided to modify print functions 
    behavior.
    @param message <any>:
        Values printed to standard error
    @params kwargs <print()>
        Key words to modify print function behavior
    """
    print(*message, file=sys.stderr, **kwargs)



def fatal(*message, **kwargs):
    """Prints any provided args to standard error
    and exits with an exit code of 1.
    @param message <any>:
        Values printed to standard error
    @params kwargs <print()>
        Key words to modify print function behavior
    """
    err(*message, **kwargs)
    sys.exit(1)


def require(cmds, suggestions, path=None):
    """Enforces an executable is in $PATH
    @param cmds list[<str>]:
        List of executable names to check
    @param suggestions list[<str>]:
        Name of module to suggest loading for a given index
        in param cmd.
    @param path list[<str>]]:
        Optional list of PATHs to check [default: $PATH]
    """
    error = False
    for i in range(len(cmds)):
        available = which(cmds[i])
        if not available:
            error = True
            err("""\n\tFatal: {} is not in $PATH and is required during runtime!
            └── Solution: please 'module load {}' and run again!""".format(cmds[i], suggestions[i])
            )

    if error: sys.exit(1)
    
    return 


def safe_copy(source, target, resources = []):
    """Private function: Given a list paths it will recursively copy each to the
    target location. If a target path already exists, it will NOT over-write the
    existing paths data.
    @param resources <list[str]>:
        List of paths to copy over to target location
    @params source <str>:
        Add a prefix PATH to each resource
    @param target <str>:
        Target path to copy templates and required resources
    """

    for resource in resources:
        destination = os.path.join(target, resource)
        if not exists(destination):
            # Required resources do not exist
            copytree(os.path.join(source, resource), destination)


def join_jsons(templates):
    """Joins multiple JSON files to into one data structure
    Used to join multiple template JSON files to create a global config dictionary.
    @params templates <list[str]>:
        List of template JSON files to join together
    @return aggregated <dict>:
        Dictionary containing the contents of all the input JSON files
    """
    # Get absolute PATH to templates in rna-seek git repo
    repo_path = os.path.dirname(os.path.abspath(__file__))
    aggregated = {}

    for file in templates:
        with open(os.path.join(repo_path, file), 'r') as fh:
            aggregated.update(json.load(fh))

    return aggregated


def git_hash(repo_path):
    """Gets the git commit hash of the RNA-seek repo.
    @param repo_path <str>:
        Path to RNA-seek git repo
    @return githash <str>:
        Latest git commit hash
    """

    githash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd = repo_path).strip()
    # Typecast to fix python3 TypeError (Object of type bytes is not JSON serializable)
    # subprocess.check_output() returns a byte string
    githash = str(githash)

    return githash


def bind_paths(search_paths):
    """Finds additional singularity bind paths from a list of random paths. Paths are
    indexed with a compostite key containing the first two directories of an absolute
    file path to avoid issues related to shared names across the /gpfs shared network
    filesystem. For each indexed list of file paths, a common path is found. Assumes
    that the paths provided are absolute paths, the rna-seek build sub command creates
    resource file index with absolute filenames.
    @param search_paths list[<str>]:
        List of absolute file paths to find common bind paths from
    @return common_paths list[<str>]:
        Returns a list of common shared file paths to create additional singularity bind paths
    """
    common_paths = []
    indexed_paths = {}

    for ref in search_paths:
        # Skip over resources with remote URI and
        # skip over strings that are not file PATHS as
        # RNA-seek build creates absolute resource PATHS
        if ref.lower().startswith('sftp://') or \
        ref.lower().startswith('s3://') or \
        ref.lower().startswith('gs://') or \
        not ref.lower().startswith(os.sep):
            continue

        # Break up path into directory tokens
        path_list = os.path.abspath(ref).split(os.sep)
        try: # Create composite index from first two directories
            # Avoids issues created by shared /gpfs/ PATHS
            index = path_list[1:3]
            index = tuple(index)
        except IndexError:
            index = path_list[1] # ref startswith /
        if index not in indexed_paths:
            indexed_paths[index] = []
        # Create an INDEX to find common PATHS for each root child directory
        # like /scratch or /data. This prevents issues when trying to find the
        # common path betweeen these two different directories (resolves to /)
        indexed_paths[index].append(str(os.sep).join(path_list))

    for index, paths in indexed_paths.items():
        # Find common paths for each path index
        common_paths.append(os.path.dirname(os.path.commonprefix(paths)))

    return list(set(common_paths))