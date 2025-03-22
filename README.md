<!--
[![CI](https://github.com/pizza-something/iam/actions/workflows/ci.yml/badge.svg)](https://github.com/pizza-something/iam/actions?query=workflow%3ACI)
[![CD](https://github.com/pizza-something/iam/actions/workflows/cd.yml/badge.svg)](https://github.com/pizza-something/iam/actions/workflows/cd.yaml)
[![GitHub Release](https://img.shields.io/github/v/release/pizza-something/iam?style=flat&logo=github&labelColor=%23282e33&color=%237c73ff)](https://github.com/pizza-something/iam/releases)
-->
[![Lines](https://img.shields.io/endpoint?url=https%3A%2F%2Fghloc.vercel.app%2Fapi%pizza-something%iam%2Fbadge%3Ffilter%3D.py&logo=python&label=lines&color=blue)](https://github.com/search?q=repo%3Aemptybutton%2effect+language%3APython+&type=code)

## Развертывание для разработки
```bash
git clone https://github.com/emptybutton/iam.git
docker compose -f iam/deployments/dev/docker-compose.yaml up
```

В контейнере используется своё виртуальное окружение, сохранённое отдельным volume-ом, поэтому можно не пересобирать образ при изменении зависимостей.

Для ide можно сделать отдельное виртуальное окружение в папке проекта:
```bash
uv sync --extra dev --directory iam
```

> [!NOTE]
> При изменении зависимостей в одном окружении необходимо синхронизировать другое с первым:
> ```bash
> uv sync --extra dev
> ```
