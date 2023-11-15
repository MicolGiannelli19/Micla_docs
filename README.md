# Micla_docs

ok my plan is to get teh automation working next I want the automation to work when I make some changes and then push into main 
this should push to a new branch named docs or something 

after that I need to sort out the TODO issues in the make.py file after that I need to implement it into twinlab

I currently have workflow that 
1. copies the docs folder from the branch it has been pushed
2. replaces the docs folder in the docs_deployment branch with the new docs folder 

I now want to
1. Add the pdoc thing that actually updates from the documentation of my fake modules 
2. Figure out if I actually also need to run a mkdocs command in all of this 
3. make the same changes form here in twinlab by branches off of Alexanders branch 
   

WARNING: when doing the thing in twinlab some issues may arries because I am not sure if you are allowed to use a workflow to push, to get arround this we might either have to work with Github secrets or change the allowences of what the github workflows are allowed to do in settings

TODO: I also should do some manual testings to see if things are changed manually or pushed in the wromg order you get issues 
