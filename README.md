A tool for patching cloudify managers.

Details of all applied patches will be stored in /etc/cloudify/patch.
Backups of modified files will also be held in this location.

Example usage:
1. Make sure cfy is pointing at a test 4.1.1 manager
2. If you point at another manager (or none), you should get helpful errors<br />
`./patchify -p userrestoredef.json -c <user>@<manager IP>`

3. You will probably be told to install patch on your manager- please do.
4. Re-run the patchify command if you had to install patch, you should see the patch apply
5. Verify the patch applied successfully<br />
`cfy snapshots create test_user_snapshot`

6. Wait for the snapshot to complete<br />
`cfy snapshots download test_user_snapshot`

7. Extract the snapshot archive. If the patch worked, you should see admin_account.json and hash_salt.json in the archive.
