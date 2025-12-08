#!/bin/bash

# 远端备份目录
BASE_DIR="/var/data"

# 保留最近 7 天
KEEP_DAYS=7

# 删除早于 KEEP_DAYS 的目录
find "$BASE_DIR" -maxdepth 1 -type d -name "20*" -mtime +$KEEP_DAYS -exec rm -rf {} \;

# 可选：记录远端清理日志
echo "[$(date)] Cleaned old backups older than $KEEP_DAYS days" >> "$BASE_DIR/cleanup.log"
