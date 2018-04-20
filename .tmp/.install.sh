git init
git remote add origin https://github.com/willzhang4a58/workspacerc.git
git pull origin master
echo "source .mybashrc" >> .bashrc
echo "\$include .myinputrc" >> .inputrc
