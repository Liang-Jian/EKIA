## MacBook command

#### 安装brew
MacBook-Pro-6:Desktop le$ /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

#### 安装docker
MacBook-Pro-6:Desktop le$ brew install --cask docker
==> Downloading https://desktop.docker.com/mac/stable/amd64/64133/Docker.dmg

#### 安装v2rayx
MacBook-Pro-6:Desktop le$ brew install --cask v2rayx

#### android sdk
export PATH=${PATH}:/Users/bruceshi/Library/Android/sdk/tools
export PATH=${PATH}:/Users/bruceshi/Library/Android/sdk/platform-tools
export PATH=${PATH}:/Users/bruceshi/Library/Android/sdk/ndk-bundle


#### 命令行播放mp3
afplay audiofile.mp3

#### mac 下 vim 设置
shi@shis-MBP ~ % cp /usr/share/vim/vimrc ~/.vimrc
shi@shis-MBP ~ % source .vimrc 
```
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
    au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
```

#### termit 设置颜色
shi@shis-MBP ~ % vi .bash_profile 
```shell

# Tell ls to be colourful
export CLICOLOR=1  #是否输出颜色
export LSCOLORS=ExGxFxdaCxDaDahbadacec #指定颜色
  
# Tell grep to highlight matches
#export GREP_OPTIONS='--color=auto' #如果没有指定，则自动选择颜

```