YCM=~/.vim/bundle/YouCompleteMe

#######################
## Initialise Vundle ##
#######################
mkdir -p ~/.vim/bundle
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall
