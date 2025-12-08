#!/usr/bin/env bash
set -e

echo ">>> mac 初始化脚本开始执行..."

# 自动选择要写入的启动脚本：优先 .zshrc，其次 .bash_profile
SHELL_RC="$HOME/.zshrc"
if [ -n "$BASH_VERSION" ]; then
  SHELL_RC="$HOME/.bash_profile"
fi

echo "将写入配置文件: $SHELL_RC"

append_line() {
  local file="$1"
  local line="$2"
  mkdir -p "$(dirname "$file")"
  touch "$file"
  if ! grep -qxF "$line" "$file" 2>/dev/null; then
    echo "$line" >> "$file"
    echo "追加到 $file: $line"
  else
    echo "已存在于 $file: $line"
  fi
}

append_block_if_missing() {
  local file="$1"
  local marker="$2"
  shift 2
  local block="$*"
  mkdir -p "$(dirname "$file")"
  touch "$file"
  if ! grep -q "$marker" "$file" 2>/dev/null; then
    echo "$block" >> "$file"
    echo "追加配置块到 $file ($marker)"
  else
    echo "$file 中已有标记 $marker，跳过该配置块"
  fi
}

#######################################
# 1. 安装 Homebrew（使用你之前的国内脚本）
#######################################
if ! command -v brew >/dev/null 2>&1; then
  echo ">>> 未检测到 Homebrew，开始安装..."
  /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
else
  echo ">>> 已安装 Homebrew，跳过安装"
fi

#######################################
# 2. 安装 Docker、V2RayX
#######################################
echo ">>> 使用 brew 安装 Docker Desktop 和 V2RayX（如已安装会跳过）"
#brew install --cask docker || true
#brew install --cask v2rayx || true

#######################################
# 3. Android SDK 相关 PATH
#######################################
echo ">>> 配置 Android SDK PATH 到 $SHELL_RC"

append_line "$SHELL_RC" 'export PATH="$PATH:$HOME/Library/Android/sdk/tools"'
append_line "$SHELL_RC" 'export PATH="$PATH:$HOME/Library/Android/sdk/platform-tools"'
append_line "$SHELL_RC" 'export PATH="$PATH:$HOME/Library/Android/sdk/ndk-bundle"'

#######################################
# 4. CMake PATH
#######################################
echo ">>> 配置 CMake PATH 到 $SHELL_RC"

append_line "$SHELL_RC" 'export PATH="/Applications/CMake.app/Contents/bin:$PATH"'

#######################################
# 5. 终端颜色设置（ls、grep 高亮）
#######################################
echo ">>> 配置终端颜色到 $SHELL_RC"

BLOCK_TERM_COLORS=$(cat << 'EOF'

# ===== CUSTOM_TERM_COLORS_BEGIN =====
# 彩色 ls
export CLICOLOR=1
export LSCOLORS=ExGxFxdaCxDaDahbadacec

# grep 高亮匹配（新版本 grep 不推荐 GREP_OPTIONS，可用别名）
if command -v grep >/dev/null 2>&1; then
  alias grep='grep --color=auto'
fi
# ===== CUSTOM_TERM_COLORS_END =====
EOF
)

append_block_if_missing "$SHELL_RC" "CUSTOM_TERM_COLORS_BEGIN" "$BLOCK_TERM_COLORS"

#######################################
# 6. vim 配置（复制系统 vimrc + 你的配置）
#######################################
echo ">>> 配置 Vim"

VIMRC="$HOME/.vimrc"

# 如果还没有自定义 .vimrc，就先从系统模板复制一份
if [ ! -f "$VIMRC" ] && [ -f /usr/share/vim/vimrc ]; then
  cp /usr/share/vim/vimrc "$VIMRC"
  echo "已从 /usr/share/vim/vimrc 复制到 $VIMRC"
fi

BLOCK_VIM=$(cat << 'EOF'

" ===== CUSTOM_VIM_CONFIG_BEGIN =====
colorscheme default
syntax on
filetype on

set number
set cursorline
"autocmd InsertLeave * se nocul
"autocmd InsertEnter * se cul

set ruler
set laststatus=2
set statusline=\ %<%F[%1*%M%*%n%R%H]%=\ %y\ %0(%{&fileformat}\ %{&encoding}\ %c:%l/%L%)\

set tabstop=4
set softtabstop=4
set shiftwidth=4
set autoindent
set cindent
set smartindent
set scrolloff=3
set incsearch
set hlsearch

set foldmethod=indent
set foldlevel=99
nnoremap <space> @=((foldclosed(line('.')) < 0) ? 'zc' : 'zo')<CR>

if has("autocmd")
    au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") |
                \ exe "normal! g'\"" | endif
endif
" ===== CUSTOM_VIM_CONFIG_END =====
EOF
)

append_block_if_missing "$VIMRC" "CUSTOM_VIM_CONFIG_BEGIN" "$BLOCK_VIM"

#######################################
# 7. 小工具：mp3 播放 alias（用 afplay）
#######################################
echo ">>> 配置 mp3 播放 alias 到 $SHELL_RC"

# append_line "$SHELL_RC" 'alias playmp3="afplay"'

#######################################
# 完成
#######################################
echo ">>> 脚本执行完成！"
echo ">>> 请执行一次： source $SHELL_RC"
echo ">>> 或者关闭并重新打开终端，让新配置生效。"
