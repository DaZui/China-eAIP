# China EAIP Dataset

**试运行阶段：数据暂不可用于正式运行，使用前请自行核查**

**Trial Phase: Data Unavailable for Formal Operation. Verify Before Use**

https://www.eaipchina.cn/dataset

## 部署与访问

`docker compose up -d` 后，数据集后台与各期电子 AIP 网页包在**同一个域名**下访问
（`china-eaip.hanming.li` 与 `china-eaip-dataset.hanming.li` 指向同一站点）：

| 路径 | 内容 | 由谁提供 |
| --- | --- | --- |
| `/` | 数据集前端（地图可视化 Vue 应用） | `frontend` 构建产物 `bun-dist`，由 `app`(caddy) 提供 |
| `/api`、`/docs`、`/redoc`、`/openapi.json` | 数据集后台 API 与文档 | `backend`（FastAPI，8000 端口） |
| `/admin`、`/static` | Django admin 与静态文件 | `backend` |
| `/EAIP2026-10.V1.4_Web/...` | `raw/*.zip` 解压出的离线 eAIP 站点 | `app`(caddy) 直接读取 `content/` |

前端「设置」面板中的 **电子 AIP eAIP** 标签页会调用
`/api/china-eaip-datasets/EaipWebPackages`，列出已解压的各期数据包并可直接进入。

### 服务

- `extract`：一次性服务，调用 `优化.py` 把 `raw/*.zip` 解压到 `content/`，并对重复文件做硬链接去重。
  已解压的包（存在同名目录）会被跳过，重复执行无副作用。再次解压可运行 `docker compose up -d extract`。
- `backend`：`backend/` 下的 FastAPI + Django，通过 `EAIP_CONTENT_ROOT=/aip` 读取解压后的数据包。
- `frontend`：`frontend/` 下的 Vue 应用，构建产物写入 `bun-dist` 卷。
- `app`：Caddy，统一入口，路由规则见 `Caddyfile`。

### 注意

- 各期数据包必须挂在**根路径**下（`/EAIP..._Web/`）：eAIP 前端使用 vue-router 的 history 模式且未设置
  base，放到子路径下会导致站内跳转丢失前缀。
- 各期数据包 `HtmlTemplate/` 下的目录名大小写不一致（`Html` / `HTML`），而页面链接统一使用 `Html`，
  `Caddyfile` 通过 `try_files` 先探测 `HTML` 再回退 `Html`，兼容两种命名。
- 数据包内容按 365 天缓存（带 hash 的静态资源额外 `immutable`）；前端入口 `index.html` 不缓存。

