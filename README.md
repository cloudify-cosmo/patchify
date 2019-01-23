A tool for patching cloudify managers.

Details of all applied patches will be stored in /etc/cloudify/patches.
Backups of modified files will also be held in this location.

Example usage:
1. Make sure cfy is pointing at a test 4.5 manager
2. If you point at another manager (or none), you should get helpful errors<br />
`./patchify -p patch_files/test_patch_1.json --install-patch-command`
3. Verify the patch applied successfully by SSHing into the manager and checking that /opt/cloudify/test_patch_1 exists.
