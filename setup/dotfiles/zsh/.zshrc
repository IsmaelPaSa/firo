source /usr/share/zsh/share/antigen.zsh

source ~/.profile

antigen use oh-my-zsh

antigen bundle git
antigen bundle heroku
antigen bundle pip
antigen bundle lein
antigen bundle command-not-found

antigen bundle zsh-users/zsh-syntax-highlighting

antigen theme candy

antigen apply
