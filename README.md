## Bulk Username Edit Tool for Adobe Admin Console

This tool allows admin to bulk edit username in Adobe Admin Console. This tool utilizes [User Sync Tool](https://github.com/adobe-apiplatform/user-sync.py) connector-umapi.yml file and csv file.

__NOTE:__ This will only work for claimed federatedID domain that is configured to use username based login.

## Usage

```
usage: bulk_username_edit.py [-h] [-u filename] -c filename [-t]

Bulk username edit Tool for Adobe Admin Console

optional arguments:
  -h, --help            show this help message and exit
  -u filename, --umapi-config filename
                        umapi config filename (default: connector-umapi.yml)
  -c filename, --csv-input filename
                        input csv filename
  -t, --test-mode       run API action calls in test mode (does not execute
                        changes on the Adobe side). Logs what would have been
                        executed.
```

## How to run this tool
Must install required dependencies (pyYaml, umapi-client) before continue.

1. See example.csv for csv template to use for bulk edit.

2. Run the following command to load umapi config from User Sync Tool and Bulk Edit CSV file
```
python bulk_username_edit.py --umapi-config c:\user-sync\connect-umapi.yml --csv-input newusername.csv
```

## Example output

```
Connected to 5190B7C05746859A7F000101@AdobeOrg,TEST-MODE: False
changeusernametest1@example.com,success, changed username fakeusername1 -> changeusernametest1
changeusernametest2@example.com,skipped,Username is the same in the console
```