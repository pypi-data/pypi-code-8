from ftw.upgrade import UpgradeStep


class AddRegistryRecords(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.billboard.upgrades:1200')
