#!/bin/bash

# === 本地文件路径 ===
SRC_FILE="/home/pi/pwd.md"

# === 远端信息 ===
REMOTE_USER="pi"
REMOTE_HOST="centos"
REMOTE_BASE_DIR="/var/data/"

# === 生成时间戳目录名 ===
DATE=$(date +%Y%m%d)
HOUR=$(date +%H)
REMOTE_DEST_DIR="${REMOTE_BASE_DIR}/${DATE}_${HOUR}"

# === 创建远端目录并上传 ===
ssh -p 22 "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p '$REMOTE_DEST_DIR'"
rsync -azP -e "ssh -p 22" "$SRC_FILE" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DEST_DIR}/password.txt"

# === 远程触发清理脚本（每日清理过期备份） ===
# ssh -p 22 "${REMOTE_USER}@${REMOTE_HOST}" "bash ${REMOTE_BASE_DIR}/clean_old_backups.sh"

# === 本地日志记录 ===
# echo "[$(date)] Synced to remote: ${REMOTE_DEST_DIR}/password.txt" >> /home/user/password_sync.log
