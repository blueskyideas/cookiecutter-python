import requests
import json
import argparse
import os

class GitHubError(Exception):
    pass

class NoAssetFound(Exception):
    pass

class TokenNotFound(Exception):
    pass

api_url_base = "https://api.github.com/repos"

def get_asset_ids(*, token):
    with open("requirements/private_assets.json","r") as f:
        repo_list = json.load(f)

    for d in repo_list:
        url = "{}/{}/releases/tags/{}?access_token={}".format(
            api_url_base,
            d['repo'],
            d['tag_name'],
            token
        )

        rsp = requests.get(url)
        if rsp.status_code == 200:
            rsp_data = rsp.json()
            found = False
            for a in rsp_data['assets']:
                if a['name'] == d['asset_name']:
                    d['asset_id'] = a['id']
                    found = True
                    break

            if not found:
                raise NoAssetFound(d['asset_name'])
        else:
            raise GitHubError("error getting asset id for {}, status code={}".format(d['asset_name'],rsp.status_code))

        print("asset id of {} is {}".format(d['asset_name'], d['asset_id']))

    return repo_list

def download_assets(*, repo_list, token):
    for d in repo_list:
        assert "asset_id" in d

        url = "{}/{}/releases/assets/{}?access_token={}".format(
            api_url_base,
            d['repo'],
            d['asset_id'],
            token,
        )

        rsp = requests.get(url, headers={'Accept': 'application/octet-stream'})

        out_file = "private_assets/{}".format(d['asset_name'])
        with open(out_file, 'wb') as f:
            for chunk in rsp.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                        #f.flush() commented by recommendation from J.F.Sebastian

        print("downloaded {}".format(d['asset_name']))


def main(args):
    print("getting asset ids")

    token = os.environ.get('GH_API_TOKEN',None)
    if not token:
        raise TokenNotFound("GH_API_TOKEN environmental variable not set")

    repo_list = get_asset_ids(token=token)
    print("downloading assets")
    download_assets(repo_list=repo_list, token=token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download release assets from private github repositories")
    args = parser.parse_args()
    print(args)
    main(args)