#!/usr/bin/env python3
"""
Clona ou atualiza todos os repositórios de uma organização GitHub.
Requer Python 3.11+.
"""
import argparse
import os
import subprocess
import sys
import requests


def get_all_repos(org: str, token: str) -> list[dict]:
    """
    Puxa todos os repositórios de uma organização, paginação automática.
    """
    repos = []
    page = 1
    headers = {"Authorization": f"token {token}", "User-Agent": "clone-org-script"}
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def clone_or_update(repo: dict, base_dir: str) -> None:
    """
    Clona ou atualiza um repositório dado seu JSON e diretório base.
    """
    name = repo.get("name")
    clone_url = repo.get("clone_url")
    dest = os.path.join(base_dir, name)
    if not os.path.exists(dest):
        print(f"Cloning {name}...")
        subprocess.run(["git", "clone", clone_url, dest], check=True)
    else:
        print(f"Updating {name}...")
        subprocess.run(["git", "pull"], cwd=dest, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clona ou atualiza todos os repositórios de uma organização GitHub."
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Token de acesso pessoal GitHub com escopo 'repo' ou 'public_repo'",
    )
    parser.add_argument(
        "--org", required=True, help="Nome da organização no GitHub (ex: HacunaMatata)"
    )
    parser.add_argument(
        "--base-dir",
        default=os.path.expanduser("~"),
        help="Diretório onde os repositórios serão clonados (default: $HOME)",
    )
    parser.add_argument(
        "--no-forks",
        action="store_true",
        help="Se definido, ignora repositórios que são forks",
    )
    args = parser.parse_args()

    base_dir = os.path.abspath(args.base_dir)
    os.makedirs(base_dir, exist_ok=True)

    try:
        repos = get_all_repos(args.org, args.token)
    except requests.HTTPError as e:
        print(f"Erro ao acessar GitHub API: {e}", file=sys.stderr)
        sys.exit(1)

    for repo in repos:
        if args.no_forks and repo.get("fork", False):
            continue
        try:
            clone_or_update(repo, base_dir)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao processar {repo.get('name')}: {e}", file=sys.stderr)

    print("\n✔ Todos os repositórios foram processados.")


if __name__ == "__main__":
    main()
