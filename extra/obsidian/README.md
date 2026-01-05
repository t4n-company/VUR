## Obsidian template and package build for XBPS

You can build it from template file with [xbps-src](https://github.com/void-linux/void-packages?tab=readme-ov-file#quick-start)

Or use xbps package from [releases](https://github.com/nar1nari/obsidian/releases)
```shell
xbps-rindex -a *.xbps
sudo xbps-install -vR $PWD obsidian
```

Or you can add releases repository to XBPS config and let XBPS handle updates automatically.
```shell
cat << EOF > /etc/xbps.d/20-obsidian.conf
repository=https://github.com/nar1nari/obsidian/releases/latest/download
EOF
xbps-install -Su obsidian
```

### Template from [nar1nari](https://github.com/nar1nari/obsidian)
