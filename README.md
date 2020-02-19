A tool for patching cloudify managers.

Details of all applied patches will be stored in /etc/cloudify/patches.
Backups of modified files will also be held in this location.

To list or apply recommended patches:
1. Make sure that cfy is pointing at the manager/cluster you are intending to update.
2. ./patchify manager-updates list
3. ./patchify manager-updates apply  # Only necessary if there are any updates to apply

To list or apply recommended patches when offline:
1. Make sure you have cloned the latest version of this repo (this will need to be updated every time you check for recommended patches).
2. Make sure that cfy is pointing at the manager/cluster you are intending to update.
3. The following commands must be run from within the repo, or the full path to the repo's central_registry and patch_files must be provided:
  3.1 ./patchify manager-updates list -c file://$(pwd)/central_registry
  3.2 ./patchify manager-updates apply -c file://$(pwd)/central_registry -r file://$(pwd)/patch_files  # Only necessary if there are any updates to apply

To apply an individual patch:
1. Make sure cfy is pointing at a test 4.5 manager
2. If you point at another manager (or none), you should get helpful errors<br />
`./patchify apply -p patch_files/test_patch_1.json --install-patch-command`
3. Verify the patch applied successfully by SSHing into the manager and checking that /opt/cloudify/test_patch_1 exists.

To use patches from a branch that is pushed to github:
1. For listing the patches, `./patchify manager-updates list -c https://raw.githubusercontent.com/cloudify-cosmo/patchify/<BRANCH_NAME>/central_registry`
2. For applying the patches, `./patchify manager-updates apply -c https://raw.githubusercontent.com/cloudify-cosmo/patchify/<BRANCH_NAME>/central_registry -r https://raw.githubusercontent.com/cloudify-cosmo/patchify/<BRANCH_NAME>/patch_files`
