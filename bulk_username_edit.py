import yaml
import os.path
import sys
import csv
import umapi_client
import argparse


def load_config_to_dict(path):
    if os.path.isfile(path):
        file = open(path, "r")
        file_data = file.read()
        yaml_data = yaml.load(file_data)
        return yaml_data
    else:
        raise AssertionError("Unable to find file")
    return None


def connect_umapi(config, test_mode):
    server_config = config["server"]
    auth_config = config['enterprise']

    if all(k in server_config for k in ("host", "endpoint", "ims_host")):
        conn = umapi_client.Connection(org_id=auth_config["org_id"],
                                       auth_dict=auth_config, ims_host=server_config["ims_host"],
                                       user_management_endpoint="https://" + server_config["host"] + server_config[
                                           "endpoint"], test_mode=test_mode)
    else:
        conn = umapi_client.Connection(org_id=auth_config["org_id"],
                                       auth_dict=auth_config, test_mode=test_mode)
    print "Connected to " + auth_config["org_id"] + ",TEST-MODE: " + str(test_mode)
    return conn


def updateUserName(conn, email, newusername):
    query = umapi_client.UserQuery(conn, email)
    result = query.result()
    if result and not result["username"] == newusername:
        # Create action for current user
        user = umapi_client.UserAction(id_type=umapi_client.IdentityTypes.federatedID,
                                       username=result["username"], domain=result["domain"],
                                       email=result["email"])
        # update username to the new one.
        user.update(username=newusername)
        _, sent, succeeded = conn.execute_single(user, immediate=True)

        if sent > succeeded:
            print email + ',error, ' + user.errors[0]['message']
        else:
            print email + ',success, changed username ' + result["username"] + ' -> ' + newusername
    else:
        print email + ',skipped,Username is the same in the console'


def main(args):
    umapi_config = args.umapi_config
    csv_filename = args.csv_filename
    test_mode = args.test_mode

    if umapi_config and csv_filename:
        conn = connect_umapi(load_config_to_dict(umapi_config), test_mode)
        with open(csv_filename, 'rb') as f:
            try:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    updateUserName(conn, row[0], row[1])
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (csv_filename, reader.line_num, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk username edit Tool for Adobe Admin Console')
    parser.add_argument('-u', '--umapi-config',
                        help='umapi config filename (default: connector-umapi.yml)',
                        metavar='filename', dest='umapi_config', default='connector-umapi.yml')
    parser.add_argument('-c', '--csv-input',
                        help='input csv filename',
                        metavar='filename', required=True, dest='csv_filename')
    parser.add_argument('-t', '--test-mode',
                        help='run API action calls in test mode (does not execute changes on the Adobe side). Logs '
                             'what would have been executed.',
                        action='store_true', dest='test_mode')

    args = parser.parse_args()

    main(args)
