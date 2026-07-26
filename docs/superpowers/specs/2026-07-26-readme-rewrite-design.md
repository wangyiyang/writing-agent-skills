# README 重写设计

日期:2026-07-26

## 目标

重写 `writing-agent-skills` 仓库的 README,以 `npx skills`(skills.sh CLI)安装方式为主线,中英双语呈现。

## 决策(已与用户确认)

- 范围:全面重写
- 语言:中英双语
- 组织方式:双文件分离 —— `README.md`(中文,默认)+ `README.en.md`(英文),顶部互放语言切换链接
- 底部增加微信公众号二维码图片:`https://www.wangyiyang.cc/images/qrcode.jpg`(已验证 HTTP 200, image/jpeg)

## 已验证事实

- `npx skills add wangyiyang/writing-agent-skills --list` 实测可发现仓库全部 3 个 skills:
  `rss-fetcher`、`content-originality-check`、`notion-to-blog`
- CLI 常用命令:`add`(支持 `--skill`、`-a/--agent`、`-g/--global`、`--list`、`-y`)、`list`、`update`、`remove`、`find`
- 仓库地址:`github.com/wangyiyang/writing-agent-skills`

## 结构(两个文件镜像一致)

1. 标题 + 语言切换链接
2. 一句话简介
3. Skills 一览表(名称 | 简介 | 文档链接)
4. 安装
   - 推荐:`npx skills add wangyiyang/writing-agent-skills`(交互式)
     - `--list` 查看、`--skill <name>` 装单个、`-a <agent>` 指定 agent、`-g` 全局
   - 备选:手动 `git clone` 后拷贝到 agent skills 目录
5. 使用:每个 skill 一小节,保留现有关键命令示例(rss-fetcher 脚本、notion-to-blog 的 `BLOG_ROOT`),详情指向各自 `SKILL.md`
6. 管理已安装 skills:`npx skills list / update / remove` 简述
7. 项目结构(保留现有)
8. 关注公众号(二维码图片)
9. License
