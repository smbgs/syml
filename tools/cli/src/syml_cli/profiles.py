from syml_cli.clients.profiles import SymlProfileClient
from syml_cli.common import SymlServiceBasedCLI


class SymlProfilesCLI(SymlServiceBasedCLI):
    """
    Profiles command group is used to configure user-based Syml CLI profiles
    """

    def __init__(self):
        self.profiles = SymlProfileClient()
        super().__init__()

    def list(self):
        """
        Lists existing profiles in the profile names
        """
        yield self.profiles.list()
        # TODO: implement this

    def create(self, profile_name: str, base=None):
        """
        Creates the new profile using name and base

        :param profile_name: profile name
        :param base: optional profile name to copy settings from
        """
        # TODO: implement this

    def delete(self, profile_name: str, confirm=False):
        """
        Removes the existing profile
        :param profile_name: profile name
        :param confirm: by default `delete` will not remove the profile and
                        will prompt for confirmation, by passing this parameter
                        we can omit the confirmation step
        """
        # TODO: learn how to use arg aliases in python.fire
        # TODO: consider python-prompt-toolkit

    def alias(self, profile_name: str, alias_name, alias_val=None):
        """
        Updates the alias value in the profile. Useful to store long strings
        like database connection strings, urls, filesystem paths etc., so that
        they can be easily used in commands as @<alias> strings.

        :param profile_name: profile name to store the alias in
        :param alias_name: alias name (without @)
        :param alias_val: alias value (any string)
        """
        # TODO: implement this
